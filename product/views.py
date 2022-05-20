from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from product.models import Likes
from account.permissions import IsAuthor

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import status


from product import serializers
from product.models import Product, Review
from rest_framework.decorators import action, api_view
from rest_framework.views import APIView

# class Pagination(PageNumberPagination):
#     page_size = 5
#     page_size_query_param = 'page'
#     max_page_size = 1000
#     invalid_page_message = (
#         'Такой страницы не существует!'
#     )


class StandartPaginationClass(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page'
    max_page_size = 1000


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    pagination_class = StandartPaginationClass
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('owner',)
    search_fields = ('title',)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


@api_view(['POST'])
def add_to_liked(request, pk):
    product = Product.objects.get(id=pk)
    if request.user.liked.filter(product=product).exists():
        return Response('Вы уже лайкнули пост', status=status.HTTP_400_BAD_REQUEST)
    Likes.objects.create(product=product, user=request.user)
    return Response('Вы поставили лайк', status=status.HTTP_201_CREATED)


@api_view(['POST'])
def remove_from_liked(request, pk):
    product = Product.objects.get(id=pk)
    if not request.user.liked.filter(product=product).exists():
        return Response('Лайк отсутсвует на посте',status=status.HTTP_400_BAD_REQUEST)
    request.user.liked.filter(product=product).delete()
    return Response('Вы убрали лайк', status=status.HTTP_204_NO_CONTENT)


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ReviewlListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor, )