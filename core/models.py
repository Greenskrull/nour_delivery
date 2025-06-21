from django.conf import settings
from django.db import models

class Restaurant(models.Model):
    name        = models.CharField(max_length=100)
    address     = models.CharField(max_length=255)
    phone       = models.CharField(max_length=20, blank=True)
    longitude   = models.FloatField(null=True, blank=True)
    latitude    = models.FloatField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    restaurant  = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_items")
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=7, decimal_places=2)
    is_available= models.BooleanField(default=True)
    image        = models.ImageField(upload_to='menu_images/', blank=True, null=True)  # new
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.restaurant.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING',   'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    restaurant  = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="orders")
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    total       = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order       = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item   = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity    = models.PositiveIntegerField(default=1)
    price       = models.DecimalField(max_digits=7, decimal_places=2)  # snapshot of menu price

    def __str__(self):
        return f"{self.quantity} × {self.menu_item.name}"


class Review(models.Model):
    order       = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="review")
    rating      = models.PositiveSmallIntegerField()  # e.g. 1–5
    comment     = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Order #{self.order.id}"
