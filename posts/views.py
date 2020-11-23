"""
author: Sanidhya Mangal
github: sanidhyamangal
"""
from base.exceptions import BaseValidationError
from base.viewsets import BaseAPIViewSet
from user.permissions import (AllowAnyPostReadUpdateDestroyOwnerOrAdmin,
                              IsAuthenticatedOrOwnerOrAdmin)

from .mixins import LikePostMixin, PostCommentsMixin
from .models import Comment, Post
from .serializers import (ListCommentSerializer, PostCommentSerializer,
                          ReadPostSerializer, UpdateCommentSerializer,
                          WritePostSerializer)


class PostViewSet(BaseAPIViewSet, LikePostMixin, PostCommentsMixin):
    model_class = Post
    instance_name = "post"
    serializer_class = ReadPostSerializer
    permission_classes = (IsAuthenticatedOrOwnerOrAdmin, )

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


class CommentViewSet(BaseAPIViewSet):
    model_class = Comment
    serializer_class = UpdateCommentSerializer
    instance_name = "comment"
    permission_classes = (IsAuthenticatedOrOwnerOrAdmin, )

    def create(self, request, *args, **kwargs):
        raise BaseValidationError("POST method not allowed")

    def list(self, request, *args, **kwargs):
        raise BaseValidationError("List Ops not allowed")

    def retrieve(self, request, pk=None, *args, **kwargs):
        raise BaseValidationError("GET Method not allowed")
