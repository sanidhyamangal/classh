"""
author: Sanidhya Mangal
github: sanidhyamangal
"""

from base.models import BaseModel
from django.conf import settings
from django.db import models

# Create your models here.


class Post(BaseModel):
    text = models.TextField(blank=True, null=True)
    media_url = models.URLField(blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="likes")
    by = models.ForeignKey(settings.AUTH_USER_MODEL,
                           on_delete=models.SET_NULL,
                           related_name="post_by",
                           null=True)

    class Meta:
        db_table = "posts"


class Comment(BaseModel):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    by = models.ForeignKey(settings.AUTH_USER_MODEL,
                           on_delete=models.SET_NULL,
                           related_name="comment_by",
                           null=True)

    class Meta:
        db_table = "comments"
