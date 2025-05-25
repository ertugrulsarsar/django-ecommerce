from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Kategori, Urun
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def ana_sayfa(request):
    kategoriler = Kategori.objects.filter(aktif=True)
    son_urunler = Urun.objects.filter(aktif=True).order_by('-olusturma_tarihi')[:8]
    return render(request, 'urunler/ana_sayfa.html', {
        'kategoriler': kategoriler,
        'son_urunler': son_urunler
    })

def urun_detay(request, slug):
    urun = get_object_or_404(Urun, slug=slug, aktif=True)
    return render(request, 'urunler/urun_detay.html', {'urun': urun})

def urun_listele(request):
    urunler = Urun.objects.filter(aktif=True)
    kategoriler = Kategori.objects.filter(aktif=True)
    return render(request, 'urunler/urun_listesi.html', {
        'urunler': urunler,
        'kategoriler': kategoriler,
    })

def kategori_urunleri(request, slug):
    kategori = get_object_or_404(Kategori, slug=slug, aktif=True)
    urunler = Urun.objects.filter(kategori=kategori, aktif=True)
    return render(request, 'urunler/urun_listesi.html', {
        'urunler': urunler,
        'kategori': kategori,
    })

@csrf_exempt
def urun_ekle(request):
    if request.method == 'POST':
        try:
            kategori = Kategori.objects.get(id=request.POST.get('kategori'))
            urun = Urun.objects.create(
                ad=request.POST.get('ad'),
                aciklama=request.POST.get('aciklama'),
                fiyat=request.POST.get('fiyat'),
                stok=request.POST.get('stok'),
                kategori=kategori
            )
            return JsonResponse({'success': True, 'message': 'Ürün başarıyla eklendi'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Geçersiz istek'})
