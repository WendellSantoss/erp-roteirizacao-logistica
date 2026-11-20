"""Funções que gravam o catálogo fictício. Cada uma é idempotente (update_or_create).

Os estados das OSs são gravados diretamente porque o seed representa uma carteira que já existia
antes do sistema; em uso normal o estado só muda pelo ``CicloDeVidaOS`` (HU-F11).
"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from almoxarifado.models import ExecucaoKit, TipoKit
from dados_demo import catalogo
from nucleo.models import (
    Equipe,
    EstadoOS,
    OrdemServico,
    OrigemAuditoria,
    PerfilUsuario,
    Polo,
    RegistroAuditoria,
    Unidade,
)


def semear_tudo(senha: str) -> dict[str, int]:
    """Grava todo o catálogo e devolve a contagem por tabela."""
    polos = semear_polos()
    semear_usuarios(senha, polos)
    for polo in polos.values():
        semear_unidades(polo)
        semear_equipes(polo)
    semear_tipos_kit()
    semear_execucoes(polos)
    semear_ordens_servico(polos)
    return {
        "polos": Polo.objects.count(),
        "usuarios": PerfilUsuario.objects.count(),
        "unidades": Unidade.objects.count(),
        "equipes": Equipe.objects.count(),
        "tipos de kit": TipoKit.objects.count(),
        "execucoes de kit": ExecucaoKit.objects.count(),
        "ordens de servico": OrdemServico.objects.count(),
    }


def semear_polos() -> dict[str, Polo]:
    return {
        codigo: Polo.objects.update_or_create(codigo=codigo, defaults={"nome": nome})[0]
        for codigo, nome in catalogo.POLOS
    }


def semear_usuarios(senha: str, polos: dict[str, Polo]) -> None:
    for email, nome, sobrenome, perfil, ve_todos, codigos_polo in catalogo.USUARIOS:
        usuario = _criar_usuario(email, nome, sobrenome, senha)
        perfil_usuario, _ = PerfilUsuario.objects.update_or_create(
            usuario=usuario, defaults={"perfil": perfil, "pode_visualizar_todos": ve_todos}
        )
        autorizados = polos.values() if codigos_polo == ["*"] else [polos[c] for c in codigos_polo]
        perfil_usuario.polos_autorizados.set(autorizados)


def _criar_usuario(email: str, nome: str, sobrenome: str, senha: str):
    usuario, _ = get_user_model().objects.update_or_create(
        username=email,
        defaults={"email": email, "first_name": nome, "last_name": sobrenome, "is_active": True},
    )
    usuario.set_password(senha)
    usuario.save(update_fields=["password"])
    return usuario


def semear_unidades(polo: Polo) -> None:
    numero_polo = polo.codigo[-1]
    for sufixo, nome, no_escopo, latitude, longitude in catalogo.UNIDADES:
        Unidade.objects.update_or_create(
            polo=polo,
            codigo=f"UN-{numero_polo}{sufixo}",
            defaults={
                "nome": f"{nome} {polo.nome.split(' - ')[-1]}",
                "no_escopo": no_escopo,
                "latitude": latitude,
                "longitude": longitude,
            },
        )


def semear_equipes(polo: Polo) -> None:
    numero_polo = polo.codigo[-1]
    for sufixo, nome, ativa in catalogo.EQUIPES:
        Equipe.objects.update_or_create(
            polo=polo, codigo=f"EQ-{numero_polo}{sufixo}", defaults={"nome": nome, "ativa": ativa}
        )


def semear_tipos_kit() -> None:
    for codigo, nome in catalogo.TIPOS_KIT:
        TipoKit.objects.update_or_create(codigo=codigo, defaults={"nome": nome})


def semear_execucoes(polos: dict[str, Polo]) -> None:
    """Grava a execução dos últimos dias para que a trava D-1 funcione em qualquer dia próximo."""
    hoje = timezone.localdate()
    kits = {kit.codigo: kit for kit in TipoKit.objects.all()}
    for codigo_polo, execucao in catalogo.EXECUCAO_DIARIA.items():
        for dias_atras in range(1, catalogo.DIAS_DE_EXECUCAO + 1):
            for codigo_kit, quantidade in execucao.items():
                ExecucaoKit.objects.update_or_create(
                    polo=polos[codigo_polo],
                    tipo_kit=kits[codigo_kit],
                    data=hoje - timedelta(days=dias_atras),
                    defaults={"quantidade": quantidade},
                )


def semear_ordens_servico(polos: dict[str, Polo]) -> None:
    agora = timezone.now()
    for polo in polos.values():
        unidades = list(polo.unidades.filter(no_escopo=True))
        for indice in range(catalogo.OS_POR_POLO):
            ordem = _gravar_os(polo, unidades[indice % len(unidades)], indice, agora)
            if ordem.estado == EstadoOS.DESCONSIDERADA:
                _auditar_desconsideracao(ordem)


def _gravar_os(polo: Polo, unidade: Unidade, indice: int, agora) -> OrdemServico:
    tipo, especificacao, prazo = catalogo.TIPOS_SERVICO[indice % len(catalogo.TIPOS_SERVICO)]
    # Aberturas espalhadas entre 2h e 4 dias atrás: parte das OSs fica em atraso (RN-06).
    horas_atras = 2 + indice * 6
    ordem, _ = OrdemServico.objects.update_or_create(
        numero=f"2026{polo.codigo[-1]}{indice:06d}",
        polo=polo,
        defaults={
            "unidade": unidade,
            "tipo": tipo,
            "especificacao": especificacao,
            "numero_imovel": f"{100 + indice * 7}",
            "cidade": "Cidade Demo",
            "setor": f"{indice % 5 + 1:03d}",
            "quadra": f"{indice * 3 + 10:03d}",
            "abertura": agora - timedelta(hours=horas_atras),
            "prazo_horas": prazo,
            "estado": catalogo.ESTADOS_OS[indice % len(catalogo.ESTADOS_OS)],
            "prioridade": indice % 5 == 0,
        },
    )
    return ordem


def _auditar_desconsideracao(ordem: OrdemServico) -> None:
    ja_auditada = RegistroAuditoria.objects.filter(
        entidade="OrdemServico", entidade_id=ordem.pk, campo="estado"
    ).exists()
    if ja_auditada:
        return
    RegistroAuditoria.objects.create(
        polo=ordem.polo,
        entidade="OrdemServico",
        entidade_id=ordem.pk,
        campo="estado",
        valor_anterior=EstadoOS.PENDENTE,
        valor_novo=EstadoOS.DESCONSIDERADA,
        justificativa="OS aberta em duplicidade no GSAN (dado fictício de demonstração).",
        origem=OrigemAuditoria.SISTEMA,
    )
