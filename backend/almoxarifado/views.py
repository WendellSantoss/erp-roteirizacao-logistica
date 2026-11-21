"""Rotas HTTP do módulo almoxarifado. Só traduzem HTTP: regra fica em services.py."""

from dataclasses import asdict

from django.utils import timezone
from drf_spectacular.utils import OpenApiTypes, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from almoxarifado import serializers, services
from nucleo.permissoes import exige_acesso, selecao_de_polo
from nucleo.serializers import validar


class LimitesKitsView(APIView):
    permission_classes = [IsAuthenticated, exige_acesso("almoxarifado")]

    @extend_schema(parameters=[serializers.FiltroDataEntrada], responses=OpenApiTypes.OBJECT)
    def get(self, request):
        # Contrato §6: o limite é sempre de um polo específico, mesmo sendo leitura.
        polo = selecao_de_polo(request, escrita=True)
        data = validar(serializers.FiltroDataEntrada, request.query_params)["data"]
        data = data or timezone.localdate()
        limites = services.limites_do_dia(polo.polo_id, data)
        return Response(
            {
                "polo_id": polo.polo_id,
                "data_referencia": data.isoformat(),
                "kits": [asdict(limite) for limite in limites],
            }
        )


class SaidasKitsView(APIView):
    permission_classes = [IsAuthenticated, exige_acesso("almoxarifado")]

    @extend_schema(
        request=serializers.SaidaKitEntrada,
        responses={201: serializers.SaidaKitRegistrada},
    )
    def post(self, request):
        polo = selecao_de_polo(request, escrita=True)
        dados = validar(serializers.SaidaKitEntrada, request.data)
        pedido = services.PedidoSaida(polo_id=polo.polo_id, **dados)
        saida = services.registrar_saida_kit(pedido, request.user)
        return Response(serializers.SaidaKitRegistrada(saida).data, status.HTTP_201_CREATED)

    @extend_schema(
        parameters=[serializers.FiltroDataEntrada],
        responses=serializers.SaidaKitListada(many=True),
    )
    def get(self, request):
        data = validar(serializers.FiltroDataEntrada, request.query_params)["data"]
        saidas = services.listar_saidas(selecao_de_polo(request).polos_ids, data)
        return Response({"resultados": serializers.SaidaKitListada(saidas, many=True).data})
