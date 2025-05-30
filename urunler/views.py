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
    urunler = Urun.objects.all()
    kategoriler = Kategori.objects.filter(aktif=True)
    kategori = None
    q = request.GET.get('q')
    min_fiyat = request.GET.get('min_fiyat')
    max_fiyat = request.GET.get('max_fiyat')
    kategori_slug = request.GET.get('kategori')

    if kategori_slug:
        kategori = Kategori.objects.filter(slug=kategori_slug, aktif=True).first()
        if kategori:
            urunler = urunler.filter(kategori=kategori)
    if q:
        urunler = urunler.filter(ad__icontains=q)
    if min_fiyat:
        urunler = urunler.filter(fiyat__gte=min_fiyat)
    if max_fiyat:
        urunler = urunler.filter(fiyat__lte=max_fiyat)

    # Her ürün için resim yoksa placeholder ekle
    urunler_list = []
    for urun in urunler:
        if not urun.resim:
            urun.placeholder_resim = 'https://via.placeholder.com/400x300?text=Ürün+Görseli'
        else:
            urun.placeholder_resim = None
        urunler_list.append(urun)

    return render(request, 'urunler/urun_listesi.html', {
        'urunler': urunler_list,
        'kategoriler': kategoriler,
        'kategori': kategori,
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
