from django.db import models
from django.conf import settings
from apps.products.models import Urun
from apps.products.models import Adres

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('paid', 'Ödendi'),
        ('shipped', 'Kargoda'),
        ('completed', 'Tamamlandı'),
        ('cancelled', 'İptal Edildi'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Urun, through='OrderItem')
    address = models.ForeignKey(Adres, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum([item.total_price() for item in self.orderitem_set.all()])

    def __str__(self):
        return f"{self.user.username} - Sipariş #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Urun, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.fiyat * self.quantity

    def __str__(self):
        return f"{self.product.ad} x {self.quantity}" 