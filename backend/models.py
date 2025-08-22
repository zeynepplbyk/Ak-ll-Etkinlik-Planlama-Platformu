from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Kullanıcılar için özel bir manager sınıfı
class CustomUserManager(BaseUserManager):
    def create_user(self, kullanici_adi, email, sifre=None, **extra_fields):
        """
        Standart kullanıcı oluşturma metodu.
        """
        if not email:
            raise ValueError("Bir e-posta adresi gereklidir.")
        email = self.normalize_email(email)  # E-posta adresini normalize eder
        kullanici = self.model(kullanici_adi=kullanici_adi, email=email, **extra_fields)
        kullanici.set_password(sifre)  # Şifreyi güvenli bir şekilde hash'ler
        kullanici.save(using=self._db)
        return kullanici

    def create_superuser(self, kullanici_adi, email, sifre=None, **extra_fields):
        """
        Superuser (yönetici) oluşturma metodu.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(kullanici_adi, email, sifre, **extra_fields)

# Kullanıcı modelini tanımlıyoruz
class Kullanici(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    kullanici_adi = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    sifre = models.CharField(max_length=128)  # Şifre hash'lenmiş olarak saklanacak
    konum = models.CharField(max_length=100, blank=True, null=True)
    ilgi_alanlari = models.TextField(blank=True, null=True)  # CSV formatında
    ad = models.CharField(max_length=50)
    soyad = models.CharField(max_length=50)
    dogum_tarihi = models.DateField(blank=True, null=True)
    cinsiyet = models.CharField(
        max_length=10,
        choices=[('E', 'Erkek'), ('K', 'Kadın'), ('D', 'Diğer')],
        blank=True, null=True
    )
    telefon_no = models.CharField(max_length=15, blank=True, null=True)
    profil_fotografi = models.ImageField(upload_to='profil_fotograflari/', blank=True, null=True)

    # Kullanıcıya ait ekstra bilgiler ve özellikler
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Kullanıcı modelinde hangi alanların zorunlu olduğunu belirt
    USERNAME_FIELD = 'kullanici_adi'
    REQUIRED_FIELDS = ['email', 'ad', 'soyad']

    objects = CustomUserManager()

    def __str__(self):
        return self.kullanici_adi
    
    
from django.db import models


class Etkinlik(models.Model):
    KATEGORI_CHOICES = [
    ('spor', 'Spor'),
    ('muzik', 'Müzik'),
    ('resim', 'Resim'),
    ('tiyatro', 'Tiyatro'),
    ('sinema', 'Sinema'),
    ('dans', 'Dans'),
    ('edebiyat', 'Edebiyat'),
    ('yemek', 'Yemek'),
    ('teknoloji', 'Teknoloji'),
    ('seminer', 'Seminer'),
    ('konser', 'Konser'),
    ('festivaller', 'Festivaller'),
    ('konferans', 'Konferans'),
]
    id = models.AutoField(primary_key=True)
    etkinlik_adi = models.CharField(max_length=100)
    aciklama = models.TextField()
    tarih = models.DateField()
    saat = models.TimeField()
    konum = models.CharField(max_length=100)  # Adres
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES)  # Seçenekleri burada tanımlıyoruz
    konum_latitude = models.FloatField(null=True, blank=True)  # Enlem
    konum_longitude = models.FloatField(null=True, blank=True)  # Boylam
    sure = models.IntegerField(default=0)  # Süre (dakika cinsinden)
    kullanici = models.ForeignKey(Kullanici, on_delete=models.CASCADE) 

    def __str__(self):
        return self.etkinlik_adi
    
    
class OnayBekleyenEtkinlikler(models.Model):
    etkinlik_adi = models.CharField(max_length=255)
    aciklama = models.TextField()
    tarih = models.DateField()
    saat = models.TimeField()
    sure = models.IntegerField()  # Süreyi dakika cinsinden saklayabilirsiniz
    kategori = models.CharField(max_length=255)
    konum = models.CharField(max_length=255)
    konum_latitude = models.FloatField()
    konum_longitude = models.FloatField()
    kullanici_id = models.IntegerField()
    onaylanmis = models.BooleanField(default=False) 

    def __str__(self):
        return self.etkinlik_adi
    
    
from django.db import models

class Katilimci(models.Model):
    kullanici = models.ForeignKey(Kullanici, on_delete=models.CASCADE)
    etkinlik = models.ForeignKey(Etkinlik, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('kullanici', 'etkinlik')  # Kullanıcı ve etkinlik kombinasyonu benzersiz olacak

    def __str__(self):
        return f"{self.kullanici.kullanici_adi} - {self.etkinlik.etkinlik_adi}"

class Mesaj(models.Model):
    id = models.AutoField(primary_key=True)
    gonderici = models.ForeignKey(Kullanici, on_delete=models.CASCADE, related_name='gonderilen_mesajlar')
    alici = models.ForeignKey(Kullanici, on_delete=models.CASCADE, related_name='alinan_mesajlar')
    mesaj_metni = models.TextField()
    gonderim_zamani = models.DateTimeField(auto_now_add=True)
    etkinlik = models.ForeignKey(Etkinlik, on_delete=models.CASCADE, related_name='mesajlar')  # Etkinlik alanı eklendi

    def __str__(self):
        return f"Mesaj {self.id} - {self.gonderici.kullanici_adi} -> {self.alici.kullanici_adi}"


class Puan(models.Model):
    kullanici = models.ForeignKey(Kullanici, on_delete=models.CASCADE)
    puan = models.PositiveIntegerField()
    kazanilan_tarih = models.DateField()

    def __str__(self):
        return f"{self.kullanici.kullanici_adi} - {self.puan} Puan"