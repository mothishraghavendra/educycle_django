from django.db import models
from users.models import User

class Product(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('exchanged', 'Exchanged'),
        ('sold', 'Sold'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


