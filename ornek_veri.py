import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
import django
from datetime import datetime
from mongoengine import connect, disconnect
from urunler.models import Kategori, Urun, UrunOzellik

django.setup()

# Bağlantıları tazele
try:
    disconnect()
except:
    pass
connect('ecommerce')

# Kategoriler
kategoriler = [
    Kategori(isim='Elektronik', aciklama='Elektronik ürünler', slug='elektronik'),
    Kategori(isim='Giyim', aciklama='Giyim ürünleri', slug='giyim'),
    Kategori(isim='Kitap', aciklama='Kitaplar', slug='kitap'),
]
for kategori in kategoriler:
    kategori.save()

# Ürünler
urunler = [
    Urun(
        isim='iPhone 15 Pro',
        aciklama='Apple iPhone 15 Pro 256GB',
        fiyat=54999.99,
        stok=50,
        kategori=kategoriler[0],
        resimler=['https://example.com/iphone15.jpg'],
        ozellikler=[
            UrunOzellik(anahtar='Renk', deger='Titanyum'),
            UrunOzellik(anahtar='Depolama', deger='256GB'),
            UrunOzellik(anahtar='RAM', deger='8GB'),
        ],
        slug='iphone-15-pro',
    ),
    Urun(
        isim='Nike Spor Ayakkabı',
        aciklama='Nike Air Max Spor Ayakkabı',
        fiyat=2499.99,
        stok=100,
        kategori=kategoriler[1],
        resimler=['https://example.com/nike.jpg'],
        ozellikler=[
            UrunOzellik(anahtar='Renk', deger='Beyaz'),
            UrunOzellik(anahtar='Numara', deger='42'),
            UrunOzellik(anahtar='Cinsiyet', deger='Unisex'),
        ],
        slug='nike-spor-ayakkabi',
    ),
    Urun(
        isim='Python ile Web Geliştirme',
        aciklama='Django ve Flask ile Web Uygulamaları Geliştirme',
        fiyat=149.99,
        stok=200,
        kategori=kategoriler[2],
        resimler=['https://example.com/python-book.jpg'],
        ozellikler=[
            UrunOzellik(anahtar='Yazar', deger='Ahmet Yılmaz'),
            UrunOzellik(anahtar='Sayfa Sayısı', deger='450'),
            UrunOzellik(anahtar='Dil', deger='Türkçe'),
        ],
        slug='python-ile-web-gelistirme',
    ),
]
for urun in urunler:
    urun.save()

print('Örnek veriler başarıyla oluşturuldu!') 