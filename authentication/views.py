from rest_framework import mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenViewBase

from authentication.models import User
from authentication.serializers import UserSerializer, TokenObtainPairSerializer
from utilities.http_code_handler import response_formatter


class UserCreateViewAPI(mixins.CreateModelMixin, GenericViewSet):
    """
    <h2 style="color:blue">Create User API</h2>

    Create user with the following fields <br/>

    <br/>
    > Permission Scope: This api is public
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        # Get response
        response_obj = super(UserCreateViewAPI, self).create(request, *args, **kwargs)

        # Apply response formatter
        response_obj.data = response_formatter(201, response_obj.data)

        # Return Response
        return response_obj


class TokenObtainPairView(TokenViewBase):
    """
    <h2 style="color:blue">Obtain Token API</h2>

    Takes a set of user credentials and returns an access and refresh JSON web <br />
    token pair to prove the authentication of those credentials. <br />
    We use the access token everywhere <br />
    Another value is refresh token that we user whenever our access token is expired (refer to RefreshToken api) <br/>

    <br/>
    > Permission Scope: This api is public
    """
    serializer_class = TokenObtainPairSerializer
