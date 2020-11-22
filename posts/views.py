from .serializers import ReadPostSerializer, WritePostSerializer
from .models import Post
from base.viewsets import BaseAPIViewSet
from user.permissions import AllowAnyPostReadUpdateDestroyOwnerOrAdmin


class PostViewSet(BaseAPIViewSet):
    model_class = Post
    instance_name = "post"
    serializer_class = ReadPostSerializer
    permission_classes = (AllowAnyPostReadUpdateDestroyOwnerOrAdmin, )

    def get_serializer_class(self):
        if self.action == "create":
            return WritePostSerializer
        return ReadPostSerializer

    def create(self, request, *args, **kwargs):
        request.data.update({'by': self.request.user.uid})
        return super(PostViewSet, self).create(request, *args, **kwargs)
