from rest_framework import serializers

from product.models import Product, Review


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(
        source='owner.username'
    )
    reviews = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'body', 'owner', 'preview', 'reviews',)

        def create(self, validated_data):
            request = self.context.get('request')
            images_data = request.FILES
            created_product = Product.objects.create(**validated_data)
            return created_product

        def is_liked(self, product):
            user = self.context.get('request').user
            return user.liked.filter(product=product).exists()

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['reviews_detail'] = ReviewSerializer(instance.reviews.all(), many=True).data
            user = self.context.get('request').user
            if user.is_authenticated:
                representation['is_liked'] = self.is_liked(instance)
            representation['likes_count'] = instance.like.count()
            return representation

class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Review
        fields = ('id', 'body', 'owner', 'post')