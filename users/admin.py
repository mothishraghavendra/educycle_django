from django.contrib import admin

# Register your models here. it is used to reigster the models in the admin panel such that a admin can able to debug it 
from .models import User

admin.site.register(User)
