"""
author: Sanidhya Mangal
github: sanidhyamangal
"""

from rest_framework import serializers
from user.models import User

from .models import Comment, Post


class WritePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('uid', 'text', 'by', 'media_url')


class UserPostReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'uid')


class ReadPostSerializer(serializers.ModelSerializer):
    by = UserPostReadSerializer()
    likes = UserPostReadSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ListCommentSerializer(serializers.ModelSerializer):
    by = UserPostReadSerializer()

    class Meta:
        model = Comment
        exclude = ('post', )


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment', )
