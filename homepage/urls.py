from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("filtragem/", views.filtragem, name="filtragem"),
    path("contato/", views.contato, name="contato"),
    path("faq/", views.faq, name="faq"),
    path("sobrenos/", views.sobrenos, name="sobrenos"),
]
