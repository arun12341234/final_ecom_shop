from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, mobile_number, password=None, **extra_fields):
        if not email and not mobile_number:
            raise ValueError('The Email or Mobile Number field must be set')
        email = self.normalize_email(email) if email else None
        user = self.model(email=email, mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, mobile_number, password, **extra_fields)

class LoginModel(AbstractBaseUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128)  # Use a secure password storage mechanism

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Set the desired login identifier field

    def __str__(self):
        return self.email or self.mobile_number
