from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import UserManager, AbstractUser
from django.db.models.constraints import UniqueConstraint


# Create your models here.
class User(AbstractUser, BaseModel, UserManager):
    dob = models.DateField(editable=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_notified = models.BooleanField(default=True)
    is_marketing_notified = models.BooleanField(default=True)

    class Meta:
        db_table = "user"
        verbose_name_plural = "User"
        constraints = [UniqueConstraint(fields=['email'], name="unique_email")]

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
