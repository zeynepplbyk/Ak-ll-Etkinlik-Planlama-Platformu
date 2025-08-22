
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.kullanici_giris, name='kullanici_giris'),  # Giriş sayfası URL'si
    path('register/', views.kullanici_kayit, name='kullanici_kayit'),
    path('anasayfa/', views.anasayfa, name='anasayfa'),  # Ana sayfa için
    path('arayuz/', views.arayuz, name='arayuz'),  # Arayüz sayfası URL'si
    path('etkinlik/olustur/', views.etkinlik_olustur, name='etkinlik_olustur'),  # Etkinlik oluşturma URL'si
    path('katil/<int:etkinlik_id>/', views.katil, name='katil'),
    path('profilim/', views.profilim, name='profilim'), 
    path('profil-guncelle/', views.profil_guncelle, name='profil_guncelle'),
    path('sifremi-unuttum/', views.sifremi_unuttum, name='sifremi_unuttum'),
    path('login/', views.kullanici_giris, name='login'),
    path('katilan-etkinlikler/', views.katilan_etkinlikler, name='katilan_etkinlikler'),
    path('mesajlar/<int:etkinlik_id>/', views.mesajlar, name='mesajlar'),
    path('etkinlik/sil/<int:event_id>/', views.delete_event, name='delete_event'),
    path('etkinlik/guncelle/<int:event_id>/', views.update_event, name='update_event'),
    path('yonetim/', views.yonetim, name='yonetim'),
    path('kullanici_sil/<int:kullanici_id>/', views.kullanici_sil, name='kullanici_sil'),
    path('cikis/', views.cikis, name='cikis'),
    path('onay-bekleyen-etkinlikler/', views.etkinlikler_onaybekleyen, name='onaybekleyen_etkinlikler'),
    path('etkinlik/onayla/<int:etkinlik_id>/', views.etkinlik_onayla, name='etkinlik_onayla'),
    path('etkinlik-detay/<int:id>/', views.etkinlik_detay, name='etkinlik_detay'),
    path('etkinlik/duzenle/<int:etkinlik_id>/', views.etkinlik_duzenle, name='etkinlik_duzenle'),
  
]

# Medya dosyalarını sunmak için şu satırı ekleyin
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)