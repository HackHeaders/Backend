from django.contrib.auth.models import AbstractUser
from django.db import models
from core.authUser.managers import CustomUserManager

class User(AbstractUser):
    username = models.CharField(max_length=255, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, null=False, blank=False)
    passage_id = models.CharField(max_length=255, null=False, blank=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    EMAIL_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'