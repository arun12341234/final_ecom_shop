from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("cart", views.cart, name="cart"),
    path("details", views.details, name="details"),
]
