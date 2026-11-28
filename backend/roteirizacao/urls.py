from django.urls import path

from roteirizacao import views

urlpatterns = [
    path("operacoes/", views.OperacoesView.as_view(), name="operacoes"),
    path("planejamento/", views.PlanejamentoView.as_view(), name="planejamento"),
    path("rotas/", views.RotasView.as_view(), name="rotas"),
    path(
        "planejamento/finalizar/",
        views.FinalizarPlanejamentoView.as_view(),
        name="planejamento-finalizar",
    ),
    path("planejamento/arquivo-rpa/", views.ArquivoRpaView.as_view(), name="arquivo-rpa"),
]
