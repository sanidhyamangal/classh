"""
author: Sanidhya Mangal
github: sanidhyamangal
"""
from base.email import send_email
from base.exceptions import BaseValidationError
from rest_framework import serializers

from .models import ForgotPassword, User, VerifyUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        _email = validated_data.get('email', '')
        if _email:
            user = VerifyUser.objects.create()
            send_email(
                'Verify your account',
                message=
                f"Hello, Please verify your email with following code: {user.uid}",
                to_email_list=_email)
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        _password = validated_data.pop("password", None)

        if _password:
            self.instance.set_password(_password)

        return super(UserSerializer, self).update(instance, validated_data)


class ForgotPasswordSerializer(serializers.ModelSerializer):
    """
    Forgot password Serializer for handling forgot password
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ForgotPassword
        fields = ['user', 'is_used']

    def create(self, validated_data):
        _user = validated_data.get('user', '')
        forgot_password = ForgotPassword.objects.create(**{'user': _user})
        send_email(
            "Rest Your Password",
            message=
            f"Hello, Please Rest your password with following token {forgot_password.uid}",
            to_email_list=_user.email)
        return forgot_password

    def update(self, instance, validated_data):
        _password = validated_data.get('password', '')
        if _password:
            self.instance.user.set_password()

        validated_data.update(**{'is_used': True})
        return super(ForgotPasswordSerializer,
                     self).update(instance, validated_data)


class ResetForgotPasswordSerializer(serializers.ModelSerializer):
    """
    Forgot password Serializer for handling forgot password
    """
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = ForgotPassword
        fields = ['is_used', 'password', 'confirm_password']

    def validate(self, attrs):
        _password, _confirm_password = attrs.get('password'), attrs.get(
            'confirm_password')
        if (_password != _confirm_password):
            raise BaseValidationError(
                detail="Confirm password and password dont match")
        return attrs

    def update(self, instance, validated_data):
        _password = validated_data.get('password', '')
        if _password:
            self.instance.user.set_password(_password)
            self.instance.user.save()

        return super(ResetForgotPasswordSerializer,
                     self).update(instance, {'is_used': True})
