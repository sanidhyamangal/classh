"""
author: Sanidhya Mangal
github: sanidhyamangal
"""
from .serializers import ReadPostSerializer, WritePostSerializer, PostCommentSerializer, ListCommentSerializer
from .models import Post
from base.viewsets import BaseAPIViewSet
from user.permissions import AllowAnyPostReadUpdateDestroyOwnerOrAdmin
from .mixins import LikePostMixin, PostCommentsMixin


class PostViewSet(BaseAPIViewSet, LikePostMixin, PostCommentsMixin):
    model_class = Post
    instance_name = "post"
    serializer_class = ReadPostSerializer
    permission_classes = (AllowAnyPostReadUpdateDestroyOwnerOrAdmin, )

    def get_serializer_class(self):
        if self.action == "create":
            return WritePostSerializer
        if self.action == "post_comment":
            return PostCommentSerializer
        if self.action == "comments":
            return ListCommentSerializer
        return ReadPostSerializer

    def create(self, request, *args, **kwargs):
        request.data.update({'by': self.request.user.uid})
        return super(PostViewSet, self).create(request, *args, **kwargs)
