import re
from django.core.exceptions import ValidationError

def validate_phone_number(value):
    if not re.match(r'^\+?1?\d{9,15}$', value):
        raise ValidationError('Geçerli bir telefon numarası giriniz.')

def validate_zip_code(value):
    if not re.match(r'^\d{5}$', value):
        raise ValidationError('Geçerli bir posta kodu giriniz (5 haneli).')

def validate_price(value):
    if value <= 0:
        raise ValidationError('Fiyat 0\'dan büyük olmalıdır.') 