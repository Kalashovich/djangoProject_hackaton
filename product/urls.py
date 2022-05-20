from django.urls import path, include
# from product import views
from product.models import Product
from product import views


from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('products', views.ProductViewSet)


# urlpatterns = [
#     # path('products/', views.ProductViewSet.as_view()),
#     path('reviews/<int:pk>', views.ReviewDetailView.as_view()),
#     path('reviews/', views.ReviewListCreateView),
#     path('', include(router.urls)),
#
# ]



urlpatterns = [
    path('create/', views.ProductCreateView.as_view()),
    path('list/', views.ProductListView.as_view()),
    path('detail/<int:pk>/', views.ProductDetailView.as_view()),
    path('list/<int:pk>/like/', views.add_to_liked),
    path('list/<int:pk>/dislike/', views.remove_from_liked),
    path('update/<int:pk>/', views.ProductUpdateView.as_view()),
    path('delete/', views.ProductDeleteView.as_view()),

    path('reviews/', views.ReviewlListCreateView.as_view()),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view()),
]


