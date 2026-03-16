from django.urls import path
from . import views

app_name = 'exchanges'

urlpatterns = [
    # Cart pages
    path('cart/', views.cart_view, name='cart'),
    
    # Cart API endpoints
    path('api/cart/count/', views.cart_count, name='cart-count'),
    path('api/cart/', views.cart_api, name='cart-api'),
    path('api/cart/add/', views.add_to_cart, name='add-to-cart'),
    path('api/cart/remove/<int:item_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('api/cart/update/<int:item_id>/', views.update_cart_item, name='update-cart-item'),
    path('api/cart/clear/', views.clear_cart, name='clear-cart'),
]
