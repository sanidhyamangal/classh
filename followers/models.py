from django.db import models
from base.models import BaseModel
from django.conf import settings
# Create your models here.


class Followers(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="user")
    followed_by = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name="followed_by")
    requested_by = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          related_name="requested_by")
    is_private = models.BooleanField(default=False)

    class Meta:
        db_table = "followers"
        verbose_name_plural = "Followers"
