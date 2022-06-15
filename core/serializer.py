from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('id', 'username', 'password', 'name', 'photo')