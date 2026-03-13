from django.urls import path
from . import views

urlpatterns = [
    path('addproducts/',views.addproducts,name='addproducts'),
    # path('',views.product_list,name="product_list"),
]