from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
from .managers import CustomUserManager
# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('USER', 'Normal User'),
        ('RECYCLER', 'Recycler')
    )

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True,verbose_name='email address')
    first_name = models.CharField(max_length=25, blank=True, verbose_name='first name')
    last_name = models.CharField(max_length=25, blank=True, verbose_name='last name')
    phone_number = models.CharField(max_length=13, blank=True, verbose_name='phone number')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return f"{self.email} ({self.role})"
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    address = models.TextField(blank=True, verbose_name='address')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    def __str__(self):
        return f"Profile of {self.user.email}"