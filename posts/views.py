from .serializers import ReadPostSerializer, WritePostSerializer
from .models import Post
from base.viewsets import BaseAPIViewSet
from base.exceptions import BaseValidationError
from user.permissions import AllowAnyPostReadUpdateDestroyOwnerOrAdmin
from rest_framework.decorators import action
from rest_framework.response import Response


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

    @action(methods=['POST'], detail=True)
    def like_dislike(self, request, *args, **kwargs):
        try:
            post = self.get_object(pk=kwargs.get('pk'))
            # import pdb;pdb.set_trace()
            _user = self.request.user.uid
            if post.likes.filter(uid=_user).exists():
                post.likes.remove(_user)
                return Response({
                    'status': True,
                    'message': 'Post disliked successfully',
                    'data': {}
                })
            post.likes.add(_user)
            return Response({
                'status': True,
                'message': 'Post liked successfully',
                'data': {}
            })
        except self.model_class.DoesNotExist:
            raise BaseValidationError("No such posts found")
