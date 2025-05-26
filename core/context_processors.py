from urunler.models import Kategori

def kategoriler_context(request):
    return {
        'kategoriler': Kategori.objects.filter(aktif=True)
    } 