from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime

from .models import Cart, CartItem
from items.models import Product
from users.models import User


@login_required
@require_http_methods(["GET"])
def cart_count(request):
    """Get the number of items in the user's cart"""
    try:
        cart = Cart.objects.get(user=request.user)
        count = cart.items.count()
        return JsonResponse({
            'success': True,
            'count': count
        })
    except Cart.DoesNotExist:
        return JsonResponse({
            'success': True,
            'count': 0
        })


@login_required
def cart_view(request):
    """Display the shopping cart page"""
    return render(request, 'exchanges/cart.html')


@login_required
@require_http_methods(["GET", "DELETE"])
def cart_api(request):
    """API endpoint to get and manage cart items"""
    
    # Get or create cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if request.method == 'GET':
        # Get all items in the cart
        cart_items = cart.items.all()
        
        items_data = []
        for item in cart_items:
            product = item.product
            # Get seller information
            seller = product.seller
            
            item_data = {
                'cart_id': item.id,
                'product_id': product.id,
                'product_name': product.title,
                'product_description': product.description or '',
                'product_price': float(product.price),
                'product_image': product.image.url if product.image else '',
                'seller_name': seller.get_full_name() or seller.username,
                'seller_phone': seller.phone_number or '',
                'product_status': product.status,
                'quantity': item.quantity,
            }
            items_data.append(item_data)
        
        total = cart.total_price
        
        return JsonResponse({
            'success': True,
            'cart_items': items_data,
            'total': float(total),
            'item_count': len(items_data)
        })
    
    elif request.method == 'DELETE':
        # Delete a specific item from cart
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Item removed from cart',
                'total': float(cart.total_price)
            })
        except CartItem.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Cart item not found'
            }, status=404)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request'
            }, status=400)


@login_required
@require_http_methods(["POST"])
def add_to_cart(request):
    """Add a product to the cart"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        # Validate product exists
        product = get_object_or_404(Product, id=product_id)
        
        # Get or create cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Add or update item in cart
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not item_created:
            # If item already exists, update quantity
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart',
            'cart_count': cart.items.count(),
            'total': float(cart.total_price)
        })
    
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Product not found'
        }, status=404)
    except (json.JSONDecodeError, ValueError) as e:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request data'
        }, status=400)


@login_required
@require_http_methods(["POST"])
def remove_from_cart(request, item_id):
    """Remove an item from the cart"""
    try:
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart',
            'cart_count': cart.items.count(),
            'total': float(cart.total_price)
        })
    
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return JsonResponse({
            'success': False,
            'message': 'Item not found'
        }, status=404)


@login_required
@require_http_methods(["POST"])
def update_cart_item(request, item_id):
    """Update quantity of an item in the cart"""
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1:
            return JsonResponse({
                'success': False,
                'message': 'Quantity must be at least 1'
            }, status=400)
        
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart updated',
            'item_total': float(cart_item.total_price),
            'cart_total': float(cart.total_price)
        })
    
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return JsonResponse({
            'success': False,
            'message': 'Item not found'
        }, status=404)
    except (json.JSONDecodeError, ValueError) as e:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request data'
        }, status=400)


@login_required
@require_http_methods(["POST"])
def clear_cart(request):
    """Clear all items from the cart"""
    try:
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart cleared',
            'cart_count': 0,
            'total': 0
        })
    
    except Cart.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Cart not found'
        }, status=404)
