from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password
import string
import random

class users_manager(BaseUserManager):
    def create_user(self, email, phone, name, password=None):
        user = self.model(email=self.normalize_email(email),
                          phone=phone,
                          name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, name, password=None):
        superuser = CustomUser.objects.create(email=self.normalize_email(email), phone=phone, name=name,
                            password=make_password(password))
        superuser.is_admin = True
        superuser.save()
        return superuser

class CustomUser(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=25, null=False, blank=False, default=True)
    email = models.EmailField(max_length=50, null=False, blank=False, unique=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    # password = models.CharField(max_length=1024, null=True, blank=True)
    emp_code = models.CharField(max_length=10, null=True, unique=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone"]

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = users_manager()
    
    # ... your model methods
    
    def has_perm(self, perm, obj=None):
        # Override this method to check for admin privileges
        if self.is_admin:
            return True
        return super().has_perm(perm, obj)

    def __str__(self):
        return self.email
    


# class ResetPassword(models.Model):
#     user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # key = models.CharField(max_length=25, null=True, blank=True)
    # time = models.DateTimeField(auto_now_add=False)

# accounts/signals.py

class ResetPassword(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    key = models.CharField(max_length=25, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.user_id.username