from django.urls import path

from nucleo import views

urlpatterns = [
    path("auth/login/", views.LoginView.as_view(), name="auth-login"),
    path("auth/me/", views.UsuarioAtualView.as_view(), name="auth-me"),
    path("auth/logout/", views.LogoutView.as_view(), name="auth-logout"),
    path("ordens-servico/", views.OrdensServicoView.as_view(), name="ordens-servico"),
    path(
        "ordens-servico/<int:ordem_id>/prioridade/",
        views.PrioridadeView.as_view(),
        name="ordem-prioridade",
    ),
    path(
        "ordens-servico/<int:ordem_id>/desconsiderar/",
        views.DesconsiderarView.as_view(),
        name="ordem-desconsiderar",
    ),
    path("auditoria/", views.AuditoriaView.as_view(), name="auditoria"),
    path("equipes/", views.EquipesView.as_view(), name="equipes"),
]
