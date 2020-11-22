from rest_framework import serializers
from .models import Comment, Post
from user.models import User


class WritePostSerializer(serializers.ModelSerializer):
    # by = serializers.PrimaryKeyRelatedField()
    class Meta:
        model = Post
        fields = ('uid', 'text', 'by', 'media_url')


class UserPostReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'uid')


class ReadPostSerializer(serializers.ModelSerializer):
    by = UserPostReadSerializer()

    class Meta:
        model = Post
        fields = '__all__'
        depth = 1
