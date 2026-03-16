from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


## The AbstractUser will create the fields like username, password, first_name, last_name, email, etc. We can add our custom fields to this model as per our requirements. In this case, we are adding phone_number field which is unique and also email field is set to unique.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message='Phone number must be exactly 10 digits.',
        code='invalid_phone'
    )
    phone_number = models.CharField(max_length=10, unique=True, validators=[phone_validator])
    LOCATION_CHOICES = [
        ('alluri_sitharama_raju', 'Alluri Sitharama Raju'),
        ('anakapalli', 'Anakapalli'),
        ('ananthapuramu', 'Ananthapuramu'),
        ('annamayya', 'Annamayya'),
        ('bapatla', 'Bapatla'),
        ('chittoor', 'Chittoor'),
        ('east_godavari', 'East Godavari'),
        ('eluru', 'Eluru'),
        ('guntur', 'Guntur'),
        ('kakinada', 'Kakinada'),
        ('konaseema', 'Konaseema'),
        ('krishna', 'Krishna'),
        ('kurnool', 'Kurnool'),
        ('nandyal', 'Nandyal'),
        ('ntr', 'NTR'),
        ('palnadu', 'Palnadu'),
        ('parvathipuram_manyam', 'Parvathipuram Manyam'),
        ('prakasam', 'Prakasam'),
        ('srikakulam', 'Srikakulam'),
        ('spsr_nellore', 'Sri Potti Sriramulu Nellore'),
        ('sri_sathya_sai', 'Sri Sathya Sai'),
        ('tirupati', 'Tirupati'),
        ('visakhapatnam', 'Visakhapatnam'),
        ('vizianagaram', 'Vizianagaram'),
        ('west_godavari', 'West Godavari'),
        ('ysr_kadapa', 'YSR Kadapa'),
        ('other', 'Other'),
    ]

    location = models.CharField(
        max_length=50,
        choices=LOCATION_CHOICES,
        default='Ananthapuramu'
    )
    def __str__(self):
        return self.username



# Create your models here.
