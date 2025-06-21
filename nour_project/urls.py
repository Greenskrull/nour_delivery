# nour_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import (
    RestaurantViewSet, MenuItemViewSet,
    OrderViewSet, ReviewViewSet,
    signup, logout_view,  # import signup directly
)
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
router.register(r'menu-items', MenuItemViewSet, basename='menuitem')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('core.urls')),
    path('api-auth/', include('rest_framework.urls')),

    # Authentication
    path('accounts/login/', 
         auth_views.LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('accounts/logout/', 
         logout_view,
         name='logout'),
    path('accounts/signup/', 
         signup, 
         name='signup'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
