from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("cart", views.cart, name="cart"),
    path("list_product", views.list_product, name="list_product"),
    path("list_product_details", views.list_product_details, name="list_product_details"),
    path("forget_password", views.forget_password, name="forget_password"),
    path('logout/', views.logout_view, name='logout'),
    path("<int:generated_org_id>/", views.generated_org_id, name="generated_org_id"),
]
