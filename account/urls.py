from django.urls import path
from account import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.RegisterApiView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('password-change/', views.NewPasswordView.as_view()),
    path('password-reset/', views.ResetPasswordView.as_view()),
    path('activate/<uuid:activation_code>/', views.ActivationCodeView.as_view()),





]