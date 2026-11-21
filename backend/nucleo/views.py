"""Rotas do núcleo: só traduzem HTTP e chamam os services (AGENTS.md §2)."""

from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from nucleo import serializers, services, sessao
from nucleo.consultas import banco_disponivel
from nucleo.permissoes import exige_acesso, selecao_de_polo
from nucleo.serializers import validar


@extend_schema(auth=[], responses={200: dict, 503: dict})
@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def health_check(request):
    if banco_disponivel():
        return Response({"status": "API OK", "database": "Banco OK"}, status=status.HTTP_200_OK)
    return Response(
        {"status": "API OK", "database": "Erro no banco"},
        status=status.HTTP_503_SERVICE_UNAVAILABLE,
    )


# ── Autenticação (HU-019/020) ─────────────────────────────────────────────────


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(request=serializers.LoginEntrada, responses=serializers.LoginSaida)
    def post(self, request):
        dados = validar(serializers.LoginEntrada, request.data)
        sessao_aberta = sessao.entrar(dados["email"], dados["senha"])
        usuario = sessao.dados_do_usuario(sessao_aberta.usuario)
        resposta = {"access_token": sessao_aberta.token, "usuario": usuario}
        return Response(serializers.LoginSaida(resposta).data)


class UsuarioAtualView(APIView):
    @extend_schema(responses=serializers.UsuarioSaida)
    def get(self, request):
        usuario = sessao.dados_do_usuario(request.user)
        return Response(serializers.UsuarioSaida(usuario).data)


class LogoutView(APIView):
    @extend_schema(request=None, responses={204: None})
    def post(self, request):
        sessao.sair(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ── Ordens de serviço (HU-006/007/008) ────────────────────────────────────────


class OrdensServicoView(APIView):
    permission_classes = [IsAuthenticated, exige_acesso("pendencias")]

    @extend_schema(parameters=[serializers.FiltroOrdensEntrada])
    def get(self, request):
        dados = validar(serializers.FiltroOrdensEntrada, request.query_params)
        filtro = services.FiltroOrdens(
            polos_ids=selecao_de_polo(request).polos_ids,
            estado=dados["estado"],
            agora=timezone.now(),
            prioridade=dados["prioridade"],
            atrasada=dados["atrasada"],
            busca=dados["busca"].strip(),
        )
        pagina = services.listar_ordens(filtro, dados["page"], dados["page_size"])
        return Response(
            {
                "total": pagina.total,
                "contadores_por_status": pagina.contadores_por_status,
                "resultados": [serializers.ordem_com_prazos(o, p) for o, p in pagina.itens],
            }
        )


def _resumo_da_ordem(ordem, usuario) -> dict:
    return {
        "id": ordem.pk,
        "numero": ordem.numero,
        "prioridade": ordem.prioridade,
        "estado": ordem.estado,
        "desconsiderada": ordem.desconsiderada,
        "atualizado_por": usuario.get_full_name() or usuario.email,
    }


class PrioridadeView(APIView):
    permission_classes = [IsAuthenticated, exige_acesso("pendencias")]

    @extend_schema(request=serializers.PrioridadeEntrada, responses=dict)
    def patch(self, request, ordem_id: int):
        polo = selecao_de_polo(request, escrita=True)
        dados = validar(serializers.PrioridadeEntrada, request.data)
        autoria = services.Autoria(request.user, dados["justificativa"])
        ordem = services.marcar_prioridade(ordem_id, polo.polo_id, dados["prioridade"], autoria)
        return Response(_resumo_da_ordem(ordem, request.user))


class DesconsiderarView(APIView):
    permission_classes = [IsAuthenticated, exige_acesso("pendencias")]

    @extend_schema(request=serializers.DesconsiderarEntrada, responses=dict)
    def post(self, request, ordem_id: int):
        polo = selecao_de_polo(request, escrita=True)
        dados = validar(serializers.DesconsiderarEntrada, request.data)
        autoria = services.Autoria(request.user, dados["justificativa"])
        ordem = services.desconsiderar_os(ordem_id, polo.polo_id, autoria)
        resumo = _resumo_da_ordem(ordem, request.user)
        return Response({**resumo, "auditoria_registrada": True})


# ── Auditoria e equipes ───────────────────────────────────────────────────────


class AuditoriaView(APIView):
    permission_classes = [IsAuthenticated, exige_acesso("auditoria")]

    @extend_schema(
        parameters=[serializers.FiltroAuditoriaEntrada],
        responses=serializers.RegistroAuditoriaSaida(many=True),
    )
    def get(self, request):
        dados = validar(serializers.FiltroAuditoriaEntrada, request.query_params)
        polos_ids = selecao_de_polo(request).polos_ids
        registros = services.consultar_auditoria(polos_ids, dados["entidade"], dados["entidade_id"])
        saida = serializers.RegistroAuditoriaSaida(registros, many=True).data
        return Response({"resultados": saida})


class EquipesView(APIView):
    permission_classes = [IsAuthenticated, exige_acesso("equipes")]

    @extend_schema(
        parameters=[serializers.FiltroEquipesEntrada],
        responses=serializers.EquipeSaida(many=True),
    )
    def get(self, request):
        dados = validar(serializers.FiltroEquipesEntrada, request.query_params)
        equipes = services.listar_equipes(selecao_de_polo(request).polos_ids, dados["ativa"])
        return Response({"resultados": serializers.EquipeSaida(equipes, many=True).data})
