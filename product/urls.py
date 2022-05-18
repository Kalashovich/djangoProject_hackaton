from django.urls import path, include
from product import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', views.)