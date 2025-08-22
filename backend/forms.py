
# backend/forms.py
from django import forms
from .models import Kullanici

class KullaniciForm(forms.ModelForm):
    class Meta:
        model = Kullanici
        fields = [
            'kullanici_adi', 'sifre', 'email', 'konum', 'ilgi_alanlari', 
            'ad', 'soyad', 'dogum_tarihi', 'cinsiyet', 'telefon_no', 'profil_fotografi'
        ]
        widgets = {
            'dogum_tarihi': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from .models import Kullanici  # Kullanıcı modelinizi buradan import edin

class ProfilGuncelleForm(forms.ModelForm):
    class Meta:
        model = Kullanici  # Kullanıcı modelinizi kullanın
        fields = ['ad', 'soyad', 'email', 'konum', 'ilgi_alanlari', 'dogum_tarihi', 'cinsiyet', 'profil_fotografi']
        widgets = {
            'dogum_tarihi': forms.DateInput(attrs={'type': 'date'}),
        }