from django.core.management.base import BaseCommand
from urunler.models import Kategori, Urun, UrunOzellik
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Örnek kategori ve ürün verilerini yükler'

    def handle(self, *args, **kwargs):
        # Önce mevcut verileri temizle
        self.stdout.write('Mevcut veriler temizleniyor...')
        UrunOzellik.objects.all().delete()
        Urun.objects.all().delete()
        Kategori.objects.all().delete()
        self.stdout.write('Mevcut veriler temizlendi.')

        # Kategorileri oluştur
        kategoriler = {
            'Elektronik': {
                'alt_kategoriler': ['Telefonlar', 'Bilgisayarlar', 'Tabletler']
            },
            'Giyim': {
                'alt_kategoriler': ['Erkek', 'Kadın', 'Çocuk']
            },
            'Ev & Yaşam': {
                'alt_kategoriler': ['Mobilya', 'Mutfak', 'Bahçe']
            }
        }

        for ana_kategori, detay in kategoriler.items():
            kategori = Kategori.objects.create(
                ad=ana_kategori,
                slug=slugify(ana_kategori),
                aktif=True
            )
            self.stdout.write(f'Kategori oluşturuldu: {ana_kategori}')

            # Alt kategorileri oluştur
            for alt_kategori in detay['alt_kategoriler']:
                Kategori.objects.create(
                    ad=alt_kategori,
                    slug=slugify(alt_kategori),
                    ust_kategori=kategori,
                    aktif=True
                )
                self.stdout.write(f'Alt kategori oluşturuldu: {alt_kategori}')

        # Örnek ürünler
        urunler = [
            {
                'ad': 'iPhone 15 Pro',
                'aciklama': 'Apple\'ın en yeni iPhone modeli',
                'fiyat': 49999.99,
                'stok': 50,
                'kategori': 'Telefonlar',
                'ozellikler': {
                    'Renk': 'Titanyum',
                    'Depolama': '256GB',
                    'Kamera': '48MP'
                }
            },
            {
                'ad': 'MacBook Pro M3',
                'aciklama': 'Apple Silicon M3 işlemcili profesyonel dizüstü',
                'fiyat': 69999.99,
                'stok': 30,
                'kategori': 'Bilgisayarlar',
                'ozellikler': {
                    'İşlemci': 'M3 Pro',
                    'RAM': '16GB',
                    'Depolama': '512GB'
                }
            },
            {
                'ad': 'Nike Spor Ayakkabı',
                'aciklama': 'Rahat ve şık spor ayakkabı',
                'fiyat': 2499.99,
                'stok': 100,
                'kategori': 'Erkek',
                'ozellikler': {
                    'Renk': 'Siyah',
                    'Numara': '42-45',
                    'Materyal': 'Deri'
                }
            }
        ]

        for urun_data in urunler:
            kategori = Kategori.objects.get(ad=urun_data['kategori'])
            urun = Urun.objects.create(
                ad=urun_data['ad'],
                slug=slugify(urun_data['ad']),
                aciklama=urun_data['aciklama'],
                fiyat=urun_data['fiyat'],
                stok=urun_data['stok'],
                kategori=kategori,
                aktif=True
            )
            self.stdout.write(f'Ürün oluşturuldu: {urun_data["ad"]}')

            # Ürün özelliklerini ekle
            for anahtar, deger in urun_data['ozellikler'].items():
                UrunOzellik.objects.create(
                    urun=urun,
                    anahtar=anahtar,
                    deger=deger
                )

        self.stdout.write(self.style.SUCCESS('Örnek veriler başarıyla yüklendi!')) 