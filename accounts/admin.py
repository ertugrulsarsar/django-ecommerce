from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'get_status_badge')
    list_filter = ('is_staff', 'is_active', 'date_joined', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    actions = ['activate_users', 'deactivate_users']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Kişisel Bilgiler', {'fields': ('first_name', 'last_name', 'email')}),
        ('İzinler', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Önemli Tarihler', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    def get_status_badge(self, obj):
        if obj.is_active:
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

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} kullanıcı aktif edildi.')
    activate_users.short_description = 'Seçili kullanıcıları aktif et'

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} kullanıcı pasif edildi.')
    deactivate_users.short_description = 'Seçili kullanıcıları pasif et'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_users'] = User.objects.all().count()
        extra_context['active_users'] = User.objects.filter(is_active=True).count()
        extra_context['staff_users'] = User.objects.filter(is_staff=True).count()
        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)
