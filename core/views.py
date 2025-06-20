from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from .models import Restaurant, MenuItem, Order, Review
from .serializers import (
    RestaurantSerializer, MenuItemSerializer,
    OrderSerializer, ReviewSerializer
)
from django.shortcuts import redirect, render, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from .cart import Cart
from .models import MenuItem
from .forms import SignupForm

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

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
            user = form.save(commit=False)
            user.is_active = False    # Deactivate until verified
            user.save()

            # Send activation email
            current_site = get_current_site(request)
            subject = "Activate your Nour account"
            message = render_to_string("registration/activation_email.html", {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            })
            email = EmailMessage(subject, message, to=[user.email])
            email.send()

            return render(request, "registration/activation_sent.html")
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('checkout')
    else:
        return HttpResponse('Activation link is invalid!', status=400)

def logout_view(request):
    """Log out the user and redirect to home (supports GET)."""
    logout(request)
    return redirect('home')

@login_required
def checkout(request):
    if not request.user.is_active:
        return redirect('login')    # TODO: integrate Stripe here
    return render(request, 'checkout.html', {})

