from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from base.viewsets import BaseAPIViewSet
from .permissions import AllowAnyPostReadUpdateDestroyOwnerOrAdmin
from .serializers import UserSerializer
from .models import User


class UserViewSet(BaseAPIViewSet):
    model_class = User
    serializer_class = UserSerializer
    instance_name = "user"
    permission_classes = (AllowAnyPostReadUpdateDestroyOwnerOrAdmin, )

    def get_permissions(self):
        if self.action == "list":
            return [IsAdminUser()]
        return [AllowAnyPostReadUpdateDestroyOwnerOrAdmin()]

    @action(methods=["POST"], detail=False)
    def login(self, request):
        try:
            for field in ['username', 'password']:
                if not self.request.data.get(field):
                    raise ValidationError({
                        'status': False,
                        'message': f"{field} is required",
                        "data": {}
                    })

            _user = self.model_class.objects.get(
                username=self.request.data['username'])

            if not _user.check_password(self.request.data['password']):
                raise ValidationError({
                    'status': False,
                    'message': 'Incorrect password',
                    'data': {}
                })

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
            raise ValidationError({
                'status': False,
                'message': "User Doesn't Exist",
                "data": {}
            })
