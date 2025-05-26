from django.db import models
from apps.products.models import Siparis

class Payment(models.Model):
    METHOD_CHOICES = [
        ('credit_card', 'Kredi Kartı'),
        ('eft', 'Havale/EFT'),
        ('cash', 'Kapıda Ödeme'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('completed', 'Tamamlandı'),
        ('failed', 'Başarısız'),
    ]
    order = models.OneToOneField(Siparis, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order} - {self.method} - {self.status}" 