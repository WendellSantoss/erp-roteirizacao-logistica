"""Rotas HTTP do módulo importacao. Só traduzem HTTP: regra fica em services.py."""

from drf_spectacular.utils import OpenApiTypes, extend_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from importacao import serializers, services
from nucleo.permissoes import exige_acesso, selecao_de_polo
from nucleo.serializers import validar


class ImportacoesView(APIView):
    permission_classes = [IsAuthenticated, exige_acesso("importacao")]
    parser_classes = [MultiPartParser]

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {"arquivo": {"type": "string", "format": "binary"}},
            }
        },
        responses={201: serializers.ImportacaoSaida},
    )
    def post(self, request):
        polo = selecao_de_polo(request, escrita=True)
        arquivo = services.preparar_arquivo(request.FILES.getlist("arquivo"))
        pedido = services.PedidoImportacao(arquivo, polo.polo_id, request.user)
        importacao = services.importar_planilha(pedido)
        return Response(serializers.ImportacaoSaida(importacao).data, status.HTTP_201_CREATED)

    @extend_schema(
        operation_id="listar_importacoes",
        parameters=[serializers.FiltroImportacoesEntrada],
        responses=OpenApiTypes.OBJECT,
    )
    def get(self, request):
        dados = validar(serializers.FiltroImportacoesEntrada, request.query_params)
        polos_ids = selecao_de_polo(request).polos_ids
        total, importacoes = services.listar_importacoes(
            polos_ids, dados["status"], dados["page"], dados["page_size"]
        )
        resultados = serializers.ImportacaoResumoSaida(importacoes, many=True).data
        return Response({"total": total, "resultados": resultados})


class ImportacaoDetalheView(APIView):
    permission_classes = [IsAuthenticated, exige_acesso("importacao")]

    @extend_schema(responses=serializers.ImportacaoSaida)
    def get(self, request, importacao_id: int):
        polos_ids = selecao_de_polo(request).polos_ids
        importacao = services.obter_importacao(importacao_id, polos_ids)
        return Response(serializers.ImportacaoSaida(importacao).data)
