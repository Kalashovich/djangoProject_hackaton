from django.urls import path, include
from order import views

urlpatterns = [
    path('order/', views.OrderApiView.as_view()),
]