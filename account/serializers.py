from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    second_password = serializers.CharField(min_length=6, required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'password', 'second_password'
        )

    def validate(self, attrs):
        second_password = attrs.pop('second_password')
        if attrs.get('password') != second_password:
            raise serializers.ValidationError('Пароли не совпадают!')
        if not attrs.get('password').isalnum():
            raise serializers.ValidationError('Поле пароля должно содержать буквы и цифры!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден!')

        user = authenticate(username=email, password=password)
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50, required=True)
    code = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(min_length=4, required=True)
    second_password = serializers.CharField(min_length=4, required=True)

    def validate(self, attrs):
        password = attrs['password']
        second_password = attrs['second_password']
        if password != second_password:
            raise serializers.ValidationError('Пароли не совпадают')

        email = attrs['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь с этим адресом электронной почты не существует')

        code = attrs['code']
        if user.activation_code != code:
            raise serializers.ValidationError('Неверный активационный код')

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        user = data['user']

        user.set_password(data(['password']))
        user.activation_code = ''
        user.save()

        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50, required=True)
