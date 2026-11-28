"""Rotas HTTP do Roteirizador. Só traduzem HTTP: regra fica nos services."""

from django.http import HttpResponse
from drf_spectacular.utils import OpenApiTypes, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from nucleo.permissoes import exige_acesso, selecao_de_polo
from nucleo.serializers import validar
from roteirizacao import serializers, services, services_despacho

ACESSO = [IsAuthenticated, exige_acesso("roteirizador")]


def _chave(request, dados) -> services.ChavePlanejamento:
    # Planejamento é sempre de um polo específico, mesmo na leitura (HU-012 RN-L03).
    polo = selecao_de_polo(request, escrita=True)
    return services.ChavePlanejamento(polo.polo_id, dados["operacao_id"], dados["data"])


class OperacoesView(APIView):
    permission_classes = ACESSO

    @extend_schema(responses=serializers.OperacaoSaida(many=True))
    def get(self, request):
        operacoes = services.listar_operacoes()
        return Response({"resultados": serializers.OperacaoSaida(operacoes, many=True).data})


class PlanejamentoView(APIView):
    permission_classes = ACESSO

    @extend_schema(parameters=[serializers.ChavePlanejamentoEntrada], responses=OpenApiTypes.OBJECT)
    def get(self, request):
        dados = validar(serializers.ChavePlanejamentoEntrada, request.query_params)
        painel = services.consultar_painel(_chave(request, dados))
        return Response(
            {
                "operacao": serializers.OperacaoSaida(painel.operacao).data,
                "data": dados["data"].isoformat(),
                "planejamento": serializers.planejamento_saida(painel),
                "rotas": serializers.RotaSaida(painel.rotas, many=True).data,
                "ordens_aptas": [serializers.ordem_no_mapa(o) for o in painel.ordens_aptas],
            }
        )


class RotasView(APIView):
    permission_classes = ACESSO

    @extend_schema(request=serializers.RotaEntrada, responses={201: serializers.RotaSaida})
    def post(self, request):
        dados = validar(serializers.RotaEntrada, request.data)
        chave = _chave(request, dados)
        campos = {k: v for k, v in dados.items() if k not in ("operacao_id", "data")}
        rota = services.criar_rota(services.PedidoRota(chave=chave, **campos), request.user)
        return Response(serializers.RotaSaida(rota).data, status=status.HTTP_201_CREATED)


class FinalizarPlanejamentoView(APIView):
    permission_classes = ACESSO

    @extend_schema(request=serializers.ChavePlanejamentoEntrada, responses=OpenApiTypes.OBJECT)
    def post(self, request):
        dados = validar(serializers.ChavePlanejamentoEntrada, request.data)
        planejamento = services_despacho.finalizar_planejamento(
            _chave(request, dados), request.user
        )
        return Response(
            {
                "id": planejamento.pk,
                "status": planejamento.status,
                "finalizado_em": planejamento.finalizado_em,
            }
        )


class ArquivoRpaView(APIView):
    permission_classes = ACESSO

    @extend_schema(
        request=serializers.ChavePlanejamentoEntrada,
        responses={201: serializers.ArquivoDespachoSaida, 200: serializers.ArquivoDespachoSaida},
    )
    def post(self, request):
        dados = validar(serializers.ChavePlanejamentoEntrada, request.data)
        resultado = services_despacho.gerar_arquivo_rpa(_chave(request, dados), request.user)
        codigo = status.HTTP_201_CREATED if resultado.gerado_agora else status.HTTP_200_OK
        return Response(serializers.ArquivoDespachoSaida(resultado.arquivo).data, status=codigo)

    @extend_schema(parameters=[serializers.ChavePlanejamentoEntrada], responses=OpenApiTypes.BINARY)
    def get(self, request):
        dados = validar(serializers.ChavePlanejamentoEntrada, request.query_params)
        arquivo = services_despacho.arquivo_gerado(_chave(request, dados))
        resposta = HttpResponse(arquivo.conteudo, content_type="text/csv; charset=utf-8")
        resposta["Content-Disposition"] = f'attachment; filename="{arquivo.nome_arquivo}"'
        resposta["X-Hash-Sha256"] = arquivo.hash_sha256
        return resposta
