from django.urls import path
from . import views
from .views import activate


urlpatterns = [
    path('', views.home, name='home'),
    path('restaurants/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:item_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
]
