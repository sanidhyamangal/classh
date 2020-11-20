"""
Author: Sanidhya Mangal
github: sanidhyamangal
"""
from base.exceptions import BaseValidationError
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ForgotPassword
from .serializers import (ForgotPasswordSerializer,
                          ResetForgotPasswordSerializer, UserSerializer,
                          UserLoginSerializer,
                          UserForgotPasswordSwaggerSerializer,
                          ForgotPasswordResetSwaggerSerializer)


class UserActionSerializerMixin:
    def get_serializer_class(self):
        if self.action == "login":
            return UserLoginSerializer
        if self.action == "forgot_password":
            return UserForgotPasswordSwaggerSerializer
        if self.action == "reset_forgot_password":
            return ForgotPasswordResetSwaggerSerializer
        return UserSerializer


class ForgotPasswordMixin:
    forgot_password_serializer = ForgotPasswordSerializer
    forgot_password_model = ForgotPassword
    reset_forgot_password_serializer = ResetForgotPasswordSerializer

    def get_forgot_password_serializer_class(self):
        assert self.forgot_password_serializer is not None, (
            "'%s' should either include `read_serializer_class` attribute"
            "or override `get_read_serializer_class()` method." %
            self.__class__.__name__)

        return self.forgot_password_serializer

    def get_forgot_password_model(self):
        assert self.forgot_password_model is not None, (
            "'%s' should either include `read_serializer_class` attribute"
            "or override `get_read_serializer_class()` method." %
            self.__class__.__name__)

        return self.forgot_password_model

    @action(methods=['POST'], detail=False, url_name="forgot_password")
    def forgot_password(self, request, *args, **kwargs):
        try:
            _email = request.data.get('email', '')
            if not _email:
                raise BaseValidationError(detail=f"Email is a required field")

            _user = self.model_class.objects.get(email=_email)
            serializer = self.get_forgot_password_serializer_class()(
                data={
                    'user': _user.uid
                })

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': True,
                    'message': 'Code successfully sent on registered email id',
                    'data': {}
                })
        except self.model_class.DoesNotExist:
            raise BaseValidationError(detail=f"No user found with {_email}")

    @action(methods=['POST'],
            detail=False,
            url_path="reset-forgot-password/(?P<token>[^/.]+)")
    def reset_forgot_password(self, request, *args, **kwargs):
        try:
            if not request.data.get('password'):
                raise BaseValidationError(detail=f"password is required")

            token = kwargs.pop('token')
            obj = self.forgot_password_model.objects.get(pk=token)
            if obj.is_used:
                raise BaseValidationError(detail=f"Token already used")

            serializer = self.reset_forgot_password_serializer(
                obj, request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    'status': True,
                    'message': 'Password updated successfully',
                    'data': {}
                })
        except self.forgot_password_model.DoesNotExist:
            raise BaseValidationError(detail=f"Not a valid token")
