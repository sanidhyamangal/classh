"""
author: Sanidhya Mangal
github: sanidhyamangal
"""
from base.models import BaseModel
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models.constraints import UniqueConstraint

from .utils import generate_token


# Create your models here.
class User(AbstractUser, BaseModel, UserManager):
    """
    ORM Model for User
    """
    dob = models.DateField(editable=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_notified = models.BooleanField(default=True)
    is_marketing_notified = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = "user"
        verbose_name_plural = "User"
        constraints = [UniqueConstraint(fields=['email'], name="unique_email")]

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name


class ForgotPassword(BaseModel):
    """
    ORM model for Forgot
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = "forgot_password"
        verbose_name_plural = "ForgotPassword"


class VerifyUser(BaseModel):
    """
    ORM model for Verify User using a token
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_used = models.BooleanField(default=False)
