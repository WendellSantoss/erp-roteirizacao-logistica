from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()
        return Response(
            {"status": "API OK", "database": "Banco OK"},
            status=status.HTTP_200_OK,
        )
    except Exception as exc:
        return Response(
            {"status": "API OK", "database": "Erro no banco", "detail": str(exc)},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
