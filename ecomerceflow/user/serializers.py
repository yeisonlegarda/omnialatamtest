from django.contrib.auth import get_user_model, authenticate
from rest_framework.serializers import ModelSerializer, Serializer, \
    ValidationError, CharField
from django.utils.translation import ugettext_lazy as _


class UsersSerializer(ModelSerializer):
    """Serialiazer for user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name', 'address')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Creates an user on system"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Updates user information"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class TokenSerializer(Serializer):
    """Serializer for token object"""
    email = CharField()
    password = CharField(
        style={'input-type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """validate and authenticates user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            requests=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Not user provided cannot authenticate')
            raise ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs
