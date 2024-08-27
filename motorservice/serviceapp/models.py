# serviceapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'  # Use username as the unique field for authentication
    REQUIRED_FIELDS = []  # No additional fields are required for superusers

    def __str__(self):
        return self.username



class Appointment(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    location_type = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Appointment for {self.name} - {self.service}"