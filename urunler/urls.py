from django.urls import path
from . import views

app_name = 'urunler'

urlpatterns = [
    path('', views.urun_listele, name='ana_sayfa'),
    path('urun/<slug:slug>/', views.urun_detay, name='urun_detay'),
    path('kategori/<slug:slug>/', views.kategori_urunleri, name='kategori_urunleri'),
] 