from django.contrib import admin
from django.db.models import Count, Sum
from django.utils.html import format_html
from .models import Kategori, Urun, UrunOzellik

class UrunOzellikInline(admin.TabularInline):
    model = UrunOzellik
    extra = 1
    classes = ['collapse']

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('ad', 'slug', 'aktif', 'olusturma_tarihi')
    list_filter = ('aktif',)
    search_fields = ('ad',)
    prepopulated_fields = {'slug': ('ad',)}
    ordering = ('-olusturma_tarihi',)
    actions = ['activate_categories', 'deactivate_categories']

    def get_status_badge(self, obj):
        if obj.aktif:
            color = 'success'
            text = 'Aktif'
        else:
            color = 'danger'
            text = 'Pasif'
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color, text
        )
    get_status_badge.short_description = 'Durum'

    def activate_categories(self, request, queryset):
        updated = queryset.update(aktif=True)
        self.message_user(request, f'{updated} kategori aktif edildi.')
    activate_categories.short_description = 'Seçili kategorileri aktif et'

    def deactivate_categories(self, request, queryset):
        updated = queryset.update(aktif=False)
        self.message_user(request, f'{updated} kategori pasif edildi.')
    deactivate_categories.short_description = 'Seçili kategorileri pasif et'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_categories'] = Kategori.objects.count()
        extra_context['active_categories'] = Kategori.objects.filter(aktif=True).count()
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Urun)
class UrunAdmin(admin.ModelAdmin):
    list_display = ('ad', 'kategori', 'fiyat', 'stok', 'aktif', 'olusturma_tarihi', 'urun_gorseli')
    list_filter = ('kategori', 'aktif')
    search_fields = ('ad', 'aciklama')
    prepopulated_fields = {'slug': ('ad',)}
    inlines = [UrunOzellikInline]
    ordering = ('-olusturma_tarihi',)
    actions = ['activate_products', 'deactivate_products', 'duplicate_products']
    
    fieldsets = (
        (None, {
            'fields': ('ad', 'slug', 'kategori', 'aciklama')
        }),
        ('Fiyat ve Stok', {
            'fields': ('fiyat', 'stok'),
            'classes': ('collapse',)
        }),
        ('Görsel', {
            'fields': ('resim',),
            'classes': ('collapse',)
        }),
        ('Durum', {
            'fields': ('aktif',),
            'classes': ('collapse',)
        }),
    )

    def urun_gorseli(self, obj):
        if obj.resim:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.resim.url)
        return "Görsel Yok"
    urun_gorseli.short_description = 'Görsel'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('kategori')

    def get_changelist_instance(self, request):
        changelist = super().get_changelist_instance(request)
        changelist.title = 'Ürün Yönetimi'
        return changelist

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_products'] = Urun.objects.count()
        extra_context['active_products'] = Urun.objects.filter(aktif=True).count()
        extra_context['total_stock'] = Urun.objects.aggregate(total=Sum('stok'))['total'] or 0
        extra_context['low_stock'] = Urun.objects.filter(stok__lt=10).count()
        
        # Kategori bazlı ürün dağılımı
        categories = Kategori.objects.all()
        category_labels = [cat.ad for cat in categories]
        category_data = [Urun.objects.filter(kategori=cat).count() for cat in categories]
        
        extra_context['category_labels'] = category_labels
        extra_context['category_data'] = category_data
        
        # Son eklenen ürünler
        extra_context['recent_products'] = Urun.objects.all().order_by('-olusturma_tarihi')[:5]
        
        return super().changelist_view(request, extra_context=extra_context)

    def get_fiyat(self, obj):
        return format_html(
            '<span class="badge bg-success">{:.2f} TL</span>',
            obj.fiyat
        )
    get_fiyat.short_description = 'Fiyat'

    def get_stok_badge(self, obj):
        if obj.stok > 10:
            color = 'success'
        elif obj.stok > 0:
            color = 'warning'
        else:
            color = 'danger'
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color, obj.stok
        )
    get_stok_badge.short_description = 'Stok'

    def get_status_badge(self, obj):
        if obj.aktif:
            color = 'success'
            text = 'Aktif'
        else:
            color = 'danger'
            text = 'Pasif'
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color, text
        )
    get_status_badge.short_description = 'Durum'

    def activate_products(self, request, queryset):
        updated = queryset.update(aktif=True)
        self.message_user(request, f'{updated} ürün aktif edildi.')
    activate_products.short_description = 'Seçili ürünleri aktif et'

    def deactivate_products(self, request, queryset):
        updated = queryset.update(aktif=False)
        self.message_user(request, f'{updated} ürün pasif edildi.')
    deactivate_products.short_description = 'Seçili ürünleri pasif et'

    def duplicate_products(self, request, queryset):
        for product in queryset:
            product.pk = None
            product.ad = f"{product.ad} (Kopya)"
            product.slug = f"{product.slug}-kopya"
            product.save()
        self.message_user(request, f'{queryset.count()} ürün kopyalandı.')
    duplicate_products.short_description = 'Seçili ürünleri kopyala'

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)
