from django.urls import path

from almoxarifado import views

urlpatterns = [
    path("limites-kits/", views.LimitesKitsView.as_view(), name="limites-kits"),
    path("saidas-kits/", views.SaidasKitsView.as_view(), name="saidas-kits"),
]
