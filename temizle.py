import os
import django
from mongoengine import connect, disconnect
from mongoengine.connection import get_db

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

# Mevcut bağlantıyı kapat
disconnect()

# MongoDB bağlantısı
connect('ecommerce')

# Tüm koleksiyonları temizle
db = get_db()
collections = ['kullanicilar', 'kategoriler', 'urunler', 'adresler', 'sepetler', 'siparisler', 'odemeler', 'degerlendirmeler']

for collection in collections:
    db[collection].drop()
    print(f"{collection} koleksiyonu silindi.")

print("\nTüm koleksiyonlar başarıyla temizlendi!") 