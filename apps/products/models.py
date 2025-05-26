from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class BaseDocument(models.Model):
    """Temel döküman sınıfı - tüm modeller için ortak özellikler"""
    aktif = models.BooleanField(default=True)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-olusturma_tarihi']

    def save(self, *args, **kwargs):
        self.guncelleme_tarihi = datetime.now()
        return super().save(*args, **kwargs)

class Kullanici(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'
        indexes = [models.Index(fields=['email', 'username'])]

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email

class Kategori(models.Model):
    """Ürün kategorileri için model"""
    ad = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    aktif = models.BooleanField(default=True)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)
    aciklama = models.TextField(max_length=500)
    ust_kategori = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'
        ordering = ['ad']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.ad)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ad

class UrunOzellik(models.Model):
    """Ürün özellikleri için gömülü döküman"""
    urun = models.ForeignKey('Urun', on_delete=models.CASCADE, related_name='ozellikler')
    anahtar = models.CharField(max_length=200)
    deger = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Ürün Özelliği'
        verbose_name_plural = 'Ürün Özellikleri'

    def __str__(self):
        return f"{self.urun.ad} - {self.anahtar}: {self.deger}"

class Urun(models.Model):
    """Ürünler için model"""
    ad = models.CharField(max_length=200)
    aciklama = models.TextField()
    fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    indirimli_fiyat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stok = models.PositiveIntegerField(default=0)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, related_name='urunler')
    resim = models.ImageField(upload_to='urunler/', null=True, blank=True)
    slug = models.SlugField(unique=True)
    aktif = models.BooleanField(default=True)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ürün'
        verbose_name_plural = 'Ürünler'
        ordering = ['-olusturma_tarihi']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.ad)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ad

    @property
    def guncel_fiyat(self):
        """İndirimli fiyat varsa onu, yoksa normal fiyatı döndürür"""
        return self.indirimli_fiyat if self.indirimli_fiyat else self.fiyat

class Adres(models.Model):
    """Kullanıcı adresleri için model"""
    kullanici_id = models.IntegerField()
    ad_soyad = models.CharField(max_length=100)
    telefon = models.CharField(max_length=20)
    adres = models.TextField()
    sehir = models.CharField(max_length=50)
    ilce = models.CharField(max_length=50)
    posta_kodu = models.CharField(max_length=10)
    varsayilan = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Adres'
        verbose_name_plural = 'Adresler'
        indexes = [models.Index(fields=['kullanici_id'])]

class SepetUrunu(models.Model):
    """Sepetteki ürünler için gömülü döküman"""
    urun = models.ForeignKey(Urun, on_delete=models.CASCADE, related_name='sepet_urunler')
    adet = models.PositiveIntegerField()
    fiyat = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def toplam_fiyat(self):
        return self.adet * self.fiyat

class Sepet(models.Model):
    """Kullanıcı sepeti için model"""
    kullanici_id = models.IntegerField()
    urunler = models.ManyToManyField(SepetUrunu, related_name='sepetler')

    @property
    def toplam_tutar(self):
        return sum(urun.toplam_fiyat for urun in self.urunler.all())

class SiparisUrunu(models.Model):
    """Siparişteki ürünler için gömülü döküman"""
    urun = models.ForeignKey(Urun, on_delete=models.CASCADE, related_name='siparis_urunler')
    adet = models.PositiveIntegerField()
    birim_fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    toplam_fiyat = models.DecimalField(max_digits=10, decimal_places=2)

class Siparis(models.Model):
    """Siparişler için model"""
    kullanici_id = models.IntegerField()
    siparis_numarasi = models.CharField(max_length=100, unique=True)
    urunler = models.ManyToManyField(SiparisUrunu, related_name='siparisler')
    toplam_tutar = models.DecimalField(max_digits=10, decimal_places=2)
    kargo_adresi = models.ForeignKey(Adres, on_delete=models.CASCADE, related_name='kargo_siparisler')
    fatura_adresi = models.ForeignKey(Adres, on_delete=models.CASCADE, related_name='fatura_siparisler')
    odeme_durumu = models.CharField(max_length=20, choices=[('beklemede', 'Beklemede'), ('odendi', 'Ödendi'), ('iptal', 'İptal')])
    kargo_durumu = models.CharField(max_length=20, choices=[('hazirlaniyor', 'Hazırlanıyor'), ('kargoda', 'Kargoda'), ('teslim_edildi', 'Teslim Edildi')])

    class Meta:
        verbose_name = 'Sipariş'
        verbose_name_plural = 'Siparişler'
        indexes = [models.Index(fields=['kullanici_id', 'siparis_numarasi', 'odeme_durumu', 'kargo_durumu'])]

class Odeme(models.Model):
    """Ödemeler için model"""
    siparis = models.ForeignKey(Siparis, on_delete=models.CASCADE, related_name='odemeler')
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    odeme_tipi = models.CharField(max_length=20, choices=[('kredi_karti', 'Kredi Kartı'), ('havale', 'Havale'), ('kapida_odeme', 'Kapıda Ödeme')])
    durum = models.CharField(max_length=20, choices=[('beklemede', 'Beklemede'), ('tamamlandi', 'Tamamlandı'), ('iptal', 'İptal')])
    islem_no = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Ödeme'
        verbose_name_plural = 'Ödemeler'
        indexes = [models.Index(fields=['siparis', 'islem_no', 'durum'])]

class Degerlendirme(models.Model):
    """Ürün değerlendirmeleri için model"""
    urun = models.ForeignKey(Urun, on_delete=models.CASCADE, related_name='degerlendirmeler')
    kullanici_id = models.IntegerField()
    puan = models.PositiveIntegerField()
    yorum = models.TextField()

    class Meta:
        verbose_name = 'Değerlendirme'
        verbose_name_plural = 'Değerlendirmeler'
        indexes = [models.Index(fields=['urun', 'kullanici_id'])]

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey('Urun', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.ad} - {self.rating}"

@receiver(post_save, sender=SiparisUrunu)
def update_stock_on_order(sender, instance, created, **kwargs):
    if created:
        product = instance.urun
        product.stok -= instance.adet
        product.save()
