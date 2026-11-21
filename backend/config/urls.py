from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from nucleo.views import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health", health_check, name="health-check"),
    path("api/v1/", include("nucleo.urls")),
    path("api/v1/importacoes/", include("importacao.urls")),
    path("api/v1/almoxarifado/", include("almoxarifado.urls")),
    # Documentação OpenAPI gerada a partir do código (Etapa 5, item 4).
    path("api/schema/", SpectacularAPIView.as_view(), name="openapi-schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="openapi-schema"), name="api-docs"),
]
