from django.contrib import admin
from .models import Restaurant, MenuItem, Order, OrderItem, Review
from django.utils.html import format_html

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'created_at')
    search_fields = ('name', 'address')
    list_filter = ('created_at',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'is_available')
    list_filter = ('restaurant', 'is_available')
    search_fields = ('name',)
    readonly_fields = ('image_thumb',)  # show preview

    fieldsets = (
        (None, {
            'fields': ('restaurant', 'name', 'description', 'price', 'is_available')
        }),
        ('Image', {
            'fields': ('image', 'image_thumb'),
        }),
    )

    def image_thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;" />', obj.image.url)
        return "-"
    image_thumb.short_description = "Preview"
    
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('order', 'rating', 'created_at')
    search_fields = ('order__id',)
