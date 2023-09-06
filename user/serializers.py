from django.contrib.auth import authenticate
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer, TokenCreateSerializer

from user.models import User


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('email', 'first_name', 'last_name', 'phone', 'image', 'password')


class CustomTokenCreateSerializer(TokenCreateSerializer):

    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        # We changed only below line
        if self.user:  # and self.user.is_active:
            return attrs
        self.fail("invalid_credentials")
