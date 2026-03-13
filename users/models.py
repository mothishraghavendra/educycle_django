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

    def __str__(self):
        return self.username



# Create your models here.
