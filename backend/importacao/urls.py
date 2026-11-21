from django.urls import path

from importacao import views

urlpatterns = [
    path("", views.ImportacoesView.as_view(), name="importacoes"),
    path("<int:importacao_id>/", views.ImportacaoDetalheView.as_view(), name="importacao-detalhe"),
]
