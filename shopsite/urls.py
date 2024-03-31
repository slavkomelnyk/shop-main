from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("", views.index, name="index"),
    path("Music/", views.m, name="m"),
    path("basket/", views.basket, name="basket"),
    path("user/<str:name>/", views.user, name="user"),
    path("search/<str:search>/", views.search, name="search"),
    path("<int:product_id>/", views.detail, name="detail"),
    path("buy/<int:product_id>/", views.order, name="order"),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('user_menu/', views.user_menu, name='user_menu'),
    path('create_product/', views.create_product, name='create_product'),
    path('user_orders/', views.user_orders, name='user_orders'),
    path('delete/<int:product_id>/', views.delete, name="delete"),
    path('order_buy/', views.order_buy, name="order_buy"),
    path('basket/delete/<int:pr_id>/', views.dele, name='delete_from_basket'),
    path('basket/history', views.basket_history, name="basket_history"),
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


