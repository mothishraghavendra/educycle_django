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
    """AJAX endpoint to load home section (all available products)"""
    # Show all products with status 'available', excluding user's own for initial browse
    # But show all products if very few exist (to help new users)
    products = Product.objects.filter(status='available').order_by('-created_at')
    
    # If fewer than 3 products exist, show all including user's own to help them understand the system
    if products.count() < 3:
        products = Product.objects.all().order_by('-created_at')
    else:
        # Otherwise exclude user's own products
        products = products.exclude(seller=request.user)
    
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
    """AJAX endpoint - redirect to cart page"""
    return redirect('exchanges:cart')

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


@login_required
def delete_product(request, product_id):
    """Delete a product (only if user is the seller)"""
    try:
        product = Product.objects.get(id=product_id, seller=request.user)
        product.delete()
        return JsonResponse({
            'success': True,
            'message': 'Product deleted successfully'
        })
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Product not found or you do not have permission to delete it'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
def edit_product(request, product_id):
    """Edit a product (only if user is the seller)"""
    try:
        product = Product.objects.get(id=product_id, seller=request.user)
        
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                # Check if it's an AJAX request
                if request.headers.get('Accept') == 'application/json':
                    return JsonResponse({
                        'success': True,
                        'message': 'Product updated successfully'
                    })
                else:
                    # Render the form with success message
                    return render(request, 'edit_product.html', {
                        'form': form,
                        'product': product,
                        'success': True,
                        'message': 'Product updated successfully'
                    })
            else:
                # Return form with errors
                return render(request, 'edit_product.html', {
                    'form': form,
                    'product': product,
                    'errors': True
                })
        else:
            # Render edit form for GET request
            form = ProductForm(instance=product)
            return render(request, 'edit_product.html', {'form': form, 'product': product})
    
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Product not found or you do not have permission to edit it'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
def get_product_details(request, product_id):
    """Get product details as JSON"""
    try:
        product = Product.objects.get(id=product_id)
        return JsonResponse({
            'success': True,
            'product': {
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'price': float(product.price),
                'status': product.status,
                'image': product.image.url if product.image else None,
                'seller': {
                    'id': product.seller.id,
                    'name': product.seller.get_full_name() or product.seller.username,
                    'phone': product.seller.phone_number if hasattr(product.seller, 'phone_number') else '',
                    'location': product.seller.location if hasattr(product.seller, 'location') else ''
                }
            }
        })
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Product not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)