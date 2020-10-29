from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        _password = validated_data.pop("password", None)

        if _password:
            self.instance.set_password(_password)

        return super(UserSerializer, self).update(instance, validated_data)
