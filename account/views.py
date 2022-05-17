from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from account import serializers

from django.contrib.auth import get_user_model
from account.register_email import reset_password, confirmation_email

User = get_user_model()


class RegisterApiView(APIView):
    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                confirmation_email(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class ActivationCodeView(APIView):
    def get(self, requests, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg':'Успешно активирован!'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'msg':'Срок действия ссылки истек!'}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(TokenObtainPairView):
    serializers_class = serializers.LoginSerializer


class NewPasswordView(APIView):
    def post(self, request):
        serializer = serializers.CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Пароль успешно сменён!')


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = serializers.PasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=serializer.data.get('email'))
            user.create_activation_code()
            user.save()
            reset_password(user)
            return Response('Проверьте свою почту!')



































































