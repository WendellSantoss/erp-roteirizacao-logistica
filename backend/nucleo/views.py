from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from nucleo.consultas import banco_disponivel


@api_view(["GET"])
def health_check(request):
    if banco_disponivel():
        return Response({"status": "API OK", "database": "Banco OK"}, status=status.HTTP_200_OK)
    return Response(
        {"status": "API OK", "database": "Erro no banco"},
        status=status.HTTP_503_SERVICE_UNAVAILABLE,
    )
