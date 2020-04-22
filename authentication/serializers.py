from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User
from utilities.baseSerializer import BaseSerializer, BaseModelSerializer
from utilities.http_code_handler import response_formatter


class UserSerializer(BaseModelSerializer):
    password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_password(value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]


class TokenObtainSerializer(BaseSerializer):
    """
    Obtain Token Serializer
    """

    username_field = User.USERNAME_FIELD
    email_field = User.EMAIL_FIELD

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set username field to authenticate
        self.fields[self.username_field] = serializers.CharField(required=False)

        # Set email field to authenticate
        self.fields[self.email_field] = serializers.CharField(required=False)

        # Set password field to authenticate
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        # You can only pass email or username to obtain token
        if attrs.get(self.username_field) and attrs.get(self.email_field):
            raise ValidationError("Only email or username is required")

        # Get username field value
        username_value = attrs.get(self.username_field)

        # If you pass email get the username of email
        if attrs.get("email"):
            user = User.objects.filter(email=attrs.get("email"))
            if user.exists():
                username_value = user.get().username

        # Build authentication info based on username and password
        authenticate_kwargs = {
            self.username_field: username_value,
            'password': attrs['password'],
        }

        try:
            # Add request to authentication info
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        # Authenticate user
        self.user = authenticate(**authenticate_kwargs)

        # If there was no authenticated user return corresponding error
        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                response_formatter(401),
                'no_active_account',
            )

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError('Must implement `get_token` method for `TokenObtainSerializer` subclasses')


class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        """
        Create token for user
        :param user:
        :return:
        """
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        # Get token
        refresh = self.get_token(self.user)

        # Access token
        data['access'] = str(refresh.access_token)

        # Refresh token
        data['refresh'] = str(refresh)

        return data
