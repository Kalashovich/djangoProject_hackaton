from django.db import models
from account.models import CustomUser
from django.contrib.auth import get_user_model


User = get_user_model()


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    body = models.TextField()
    preview = models.ImageField(upload_to='Image/', blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}: {self.price}сом'

    # class Meta:
    #     ordering = ('created_at',)
    #
    #     def __str__(self):
    #         return f'{self.title}: {self.price}сом'


class Review(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='reviews', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} - {self.body} - {self.created_at}'


class Likes(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked')

    class Meta:
        unique_together = ['product', 'user']

























































