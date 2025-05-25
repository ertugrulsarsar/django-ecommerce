from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from .models import User
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger(__name__)

# Kayıt formu
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Şifre (tekrar)', widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Şifreler eşleşmiyor!')
        return cleaned_data

# Kayıt
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Kullanıcı adı ve email kontrolü
            if User.objects.filter(username=form.cleaned_data['username']).first():
                messages.error(request, 'Bu kullanıcı adı zaten kullanılıyor!')
                return render(request, 'accounts/register.html', {'form': form})
            
            if User.objects.filter(email=form.cleaned_data['email']).first():
                messages.error(request, 'Bu email adresi zaten kullanılıyor!')
                return render(request, 'accounts/register.html', {'form': form})

            # Yeni kullanıcı oluştur
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data.get('first_name', ''),
                last_name=form.cleaned_data.get('last_name', '')
            )
            
            messages.success(request, 'Kayıt başarılı! Giriş yapabilirsiniz.')
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# Giriş
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"Giriş denemesi - Kullanıcı adı: {username}")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(f"Kullanıcı doğrulandı: {user.username}")
            login(request, user)
            messages.success(request, 'Başarıyla giriş yaptınız!')
            return redirect('urunler:ana_sayfa')
        else:
            print(f"Kullanıcı doğrulanamadı: {username}")
            messages.error(request, 'Kullanıcı adı veya şifre hatalı!')
    
    return render(request, 'accounts/login.html')

# Çıkış
@login_required
def logout_view(request):
    logout(request)
    return redirect('urunler:ana_sayfa')

# Profil
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
