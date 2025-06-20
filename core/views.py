from rest_framework import viewsets, permissions
from .models import Restaurant, MenuItem, Order, Review
from .serializers import (
    RestaurantSerializer, MenuItemSerializer,
    OrderSerializer, ReviewSerializer
)
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from .models import MenuItem

class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.AllowAny]

class MenuItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MenuItem.objects.filter(is_available=True)
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.AllowAny]

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(order__user=self.request.user)

@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(MenuItem, id=item_id, is_available=True)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(item, quantity=quantity, override_quantity=request.POST.get('override'))
    return redirect('cart_detail')

@require_POST
def cart_remove(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(MenuItem, id=item_id)
    cart.remove(item)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

def home(request):
    # Always show the first (and only) restaurant
    restaurant = get_object_or_404(Restaurant, pk=1)
    return render(request, 'home.html', {'restaurant': restaurant})
    
def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    menu_items = restaurant.menu_items.filter(is_available=True)
    return render(request, 'restaurant/detail.html', {
        'restaurant': restaurant,
        'menu_items': menu_items
    })

def checkout(request):
    # TODO: integrate Stripe here
    return render(request, 'checkout.html', {})