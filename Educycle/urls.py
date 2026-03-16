from django.contrib import admin
from django.urls import path, include
from exchanges.views import cart_count

# Import settings and static for media files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('items/',include('items.urls')),
    path('exchanges/', include('exchanges.urls')),
    path('api/cart/count/', cart_count, name='api-cart-count'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)