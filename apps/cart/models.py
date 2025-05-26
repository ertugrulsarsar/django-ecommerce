from django.db import models
from django.conf import settings
from apps.products.models import Urun

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    products = models.ManyToManyField(Urun, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum([item.total_price() for item in self.cartitem_set.all()])

    def __str__(self):
        return f"{self.user.username} - Sepet"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Urun, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.fiyat * self.quantity

    def __str__(self):
        return f"{self.product.ad} x {self.quantity}" 