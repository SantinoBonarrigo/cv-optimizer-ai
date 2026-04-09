from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("historial/", views.history, name="history"),
    path("historial/<int:pk>/", views.detail, name="detail"),
]
