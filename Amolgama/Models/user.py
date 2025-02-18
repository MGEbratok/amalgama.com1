from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class UserRegistrationForm(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length =30, null =True, blank =True) 
    describe = models.CharField(max_length =30, null =True, blank =True)
    email =models.EmailField(_("email address"), unique =True) 
    in_staff = models.BooleanField(default =False) 
    in_active = models.BooleanField(default =False)
    date_joined = models.DateTimeField(default =timezone.now)
    code = models.CharField(max_length =6, null =True, blak =True)
    is_verificated = models.BooleanField(default =False)
    
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects =CustomUserManager
    
    def __str__(self):
        return self.email