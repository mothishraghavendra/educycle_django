from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product
from exchanges.models import Exchange
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q

@login_required
def addproducts(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('dashboard')
    else:
        form = ProductForm()
    
    return render(request, 'addproducts.html', {'form': form})

@login_required
def dashboard(request):
    """Main dashboard page"""
    return render(request, 'dashboard.html')

@login_required
def get_products_section(request):
    """AJAX endpoint to load home section (other users' products)"""
    products = Product.objects.exclude(seller=request.user).order_by('-created_at')
    return render(request, 'sections/products_list.html', {'products': products, 'section': 'home'})

@login_required
def get_my_products_section(request):
    """AJAX endpoint to load my items section (current user's products)"""
    products = Product.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'sections/products_list.html', {'products': products, 'section': 'my-items'})

@login_required
def get_profile_section(request):
    """AJAX endpoint to load profile section"""
    products_count = Product.objects.filter(seller=request.user).count()
    exchanges_count = Exchange.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user),
        status='completed'
    ).count()
    
    context = {
        'user': request.user,
        'products_count': products_count,
        'exchanges_count': exchanges_count,
        'reviews_count': 0,  # Add review model later
        'rating': 4.5,  # Add rating calculation later
    }
    return render(request, 'sections/profile.html', context)

@login_required
def get_orders_section(request):
    """AJAX endpoint to load orders/exchanges section"""
    exchanges = Exchange.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user)
    ).order_by('-created_at')
    
    context = {
        'exchanges': exchanges,
    }
    return render(request, 'sections/orders.html', context)

@login_required
def get_user_data(request):
    """API endpoint to fetch user data as JSON"""
    try:
        user = request.user
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone_number': getattr(user, 'phone_number', ''),
                'location': getattr(user, 'location', 'Not set'),
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)
