from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('addproducts/', views.addproducts, name='addproducts'),
    
    # AJAX endpoints for dashboard sections
    path('api/products/', views.get_products_section, name='api_products'),
    path('api/my-products/', views.get_my_products_section, name='api_my_products'),
    path('api/profile/', views.get_profile_section, name='api_profile'),
    path('api/orders/', views.get_orders_section, name='api_orders'),
    path('api/user-data/', views.get_user_data, name='api_user_data'),
]