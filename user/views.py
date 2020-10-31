"""
author: Sanidhya Mangal
github: sanidhyamangal
"""
from base.exceptions import BaseValidationError
from base.viewsets import BaseAPIViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .mixins import ForgotPasswordMixin
from .models import User, VerifyUser
from .permissions import AllowAnyPostReadUpdateDestroyOwnerOrAdmin
from .serializers import UserSerializer


class UserViewSet(BaseAPIViewSet, ForgotPasswordMixin):
    model_class = User
    serializer_class = UserSerializer
    instance_name = "user"
    permission_classes = (AllowAnyPostReadUpdateDestroyOwnerOrAdmin, )

    def get_permissions(self):
        if self.action == "list":
            return [IsAdminUser()]
        if self.action == "verify_user":
            return [AllowAny()]
        return [AllowAnyPostReadUpdateDestroyOwnerOrAdmin()]

    @action(methods=["POST"], detail=False)
    def login(self, request):
        try:
            for field in ['username', 'password']:
                if not self.request.data.get(field):
                    raise BaseValidationError(detail=f"{field} is required")

            _user = self.model_class.objects.get(
                username=self.request.data['username'])

            if not _user.check_password(self.request.data['password']):
                raise BaseValidationError(detail=f"Incorrect Password")

            token = RefreshToken.for_user(_user)
            user_serializer = UserSerializer(_user)
            _data = user_serializer.data
            _data.update({'token': str(token.access_token)})
            return Response({
                'status': True,
                'message': 'Login Successful',
                'data': _data
            })

        except self.model_class.DoesNotExist:
            raise BaseValidationError(detail=f"User Doesn't Exists")

    @action(methods=["GET"],
            detail=False,
            url_path="verify-user/(?P<token>[^/.]+)",
            url_name="verify-user")
    def verify_user(self, request, *args, **kwargs):
        try:
            token = kwargs.pop('token')
            obj = VerifyUser.objects.get(pk=token)
            if obj.is_used:
                raise BaseValidationError(detail=f"Token already used")
            obj.is_used = True
            obj.save()
            return Response({
                'status': True,
                'message': 'User validate successfully',
                'data': {}
            })
        except VerifyUser.DoesNotExist:
            raise BaseValidationError(detail=f"Not a valid token")
