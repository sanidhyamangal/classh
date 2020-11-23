"""
author: Sanidhya Mangal
github: sanidhyamangal
"""
from rest_framework.decorators import action
from rest_framework.response import Response
from base.exceptions import BaseValidationError
from .models import Comment


class LikePostMixin:
    @action(methods=['POST'], detail=True)
    def like_dislike(self, request, *args, **kwargs):
        try:
            post = self.get_object(pk=kwargs.get('pk'))

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


class PostCommentsMixin:
    @action(methods=['POST'], detail=True)
    def post_comment(self, request, *args, **kwargs):
        if not self.model_class.objects.filter(pk=kwargs.get('pk')).exists():
            raise BaseValidationError(f"No such post found")
        _data = {
            **request.data, 'by': self.request.user.uid,
            'post': kwargs.get('pk')
        }

        serializer = self.get_serializer(data=_data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': 'Comment added sucessfully',
                'data': serializer.data
            })
        return Response({
            'status': False,
            'message': 'Adding Comment failed',
            'data': serializer.errors
        })

    @action(methods=['GET'], detail=True)
    def comments(self, request, *args, **kwargs):
        if not self.model_class.objects.filter(pk=kwargs.get('pk')).exists():
            raise BaseValidationError(f"No such post found")

        queryset = Comment.objects.filter(post=kwargs.get('pk'))
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'status': True,
            'message': 'Comments reterieved successfully',
            'data': serializer.data
        })
