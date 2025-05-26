from django.urls import path
from urunler.views import ana_sayfa, urun_listele, urun_detay, kategori_urunleri

app_name = 'urunler'

urlpatterns = [
    path('', ana_sayfa, name='ana_sayfa'),
    path('urunler/', urun_listele, name='urun_listele'),
    path('anasayfa/', ana_sayfa, name='ana_sayfa_kopya'),
    path('urun/<slug:slug>/', urun_detay, name='urun_detay'),
    path('kategori/<slug:slug>/', kategori_urunleri, name='kategori_urunleri'),
] 