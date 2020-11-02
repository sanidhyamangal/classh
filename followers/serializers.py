from .models import Followers
from rest_framework import serializers


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = ['uid', 'user', 'followed_by', 'is_private']


class FollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = ['uid', 'user', 'requested_by', 'is_private']
