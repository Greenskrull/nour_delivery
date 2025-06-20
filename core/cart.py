# core/cart.py

from decimal import Decimal
from django.conf import settings
from .models import MenuItem

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, menu_item, quantity=1, override_quantity=False):
        """Add or update a menu_item in the cart."""
        item_id = str(menu_item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {
                'quantity': 0,
                'price': str(menu_item.price)
            }
        if override_quantity:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Mark the session as “modified” so Django knows to save it
        self.session.modified = True

    def remove(self, menu_item):
        """Remove a menu_item from the cart."""
        item_id = str(menu_item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def __iter__(self):
        """Iterate over the items, fetching menu_item from DB."""
        item_ids = self.cart.keys()
        items = MenuItem.objects.filter(id__in=item_ids)
        for item in items:
            cart_item = self.cart[str(item.id)]
            cart_item['menu_item'] = item
            cart_item['total_price'] = Decimal(cart_item['price']) * cart_item['quantity']
            yield cart_item

    def __len__(self):
        """Count total items in cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # Remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
