from rest_framework.generics import CreateAPIView
from user.serializers import UsersSerializer, TokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(CreateAPIView):
    """Creates an user on system"""
    authentication_classes = {}
    permission_classes = {}
    serializer_class = UsersSerializer


class TokenAuthenticathionView(ObtainAuthToken):
    """Authenticate and get token"""
    authentication_classes = {}
    permission_classes = {}
    serializer_class = TokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES