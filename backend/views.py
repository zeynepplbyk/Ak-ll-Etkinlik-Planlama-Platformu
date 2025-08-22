import json
from urllib import request
from django.shortcuts import render, redirect
from .models import Kullanici
from django.contrib.auth.hashers import make_password
from django.contrib import messages  # Mesajları eklemek için

def kullanici_kayit(request):
    if request.method == 'POST':
        kullanici_adi = request.POST['kullanici_adi']
        sifre = request.POST['sifre']
        email = request.POST['email']
        konum = request.POST['konum']
        ilgi_alanlari = request.POST['ilgi_alanlari']
        ad = request.POST['ad']
        soyad = request.POST['soyad']
        dogum_tarihi = request.POST['dogum_tarihi']
        cinsiyet = request.POST['cinsiyet']
        telefon_no = request.POST['telefon_no']
        profil_fotografi = request.FILES.get('profil_fotografi')

        # Kullanıcı adı kontrolü
        if Kullanici.objects.filter(kullanici_adi=kullanici_adi).exists():
            return render(request, 'register.html', {'error': 'Bu kullanıcı adı zaten alınmış.'})
        
        # Yeni kullanıcı oluştur
        yeni_kullanici = Kullanici.objects.create(
            kullanici_adi=kullanici_adi,
            sifre=make_password(sifre),  # Şifreyi hashle
            email=email,
            konum=konum,
            ilgi_alanlari=ilgi_alanlari,
            ad=ad,
            soyad=soyad,
            dogum_tarihi=dogum_tarihi,
            cinsiyet=cinsiyet,
            telefon_no=telefon_no,
            profil_fotografi=profil_fotografi
        )
        
        # Kullanıcı başarıyla kaydedildi, başarı mesajı göster
        messages.success(request, 'Hesabınız başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.')
        
       
        return redirect('kullanici_giris')  
        
    return render(request, 'register.html')





from django.shortcuts import render
from .models import Kullanici  # or any other imports you need

def arayuz(request):
    # Assuming you have user-related logic here
    kullanici = Kullanici.objects.get(id=1)  # Example: Get user with ID 1
    return render(request, 'arayuz.html', {'kullanici_adi': kullanici.kullanici_adi})





from django.shortcuts import render, redirect
from .models import Etkinlik,OnayBekleyenEtkinlikler
from django.http import JsonResponse, HttpResponseBadRequest
from geopy.geocoders import Nominatim
import json
def etkinlik_olustur(request):
    if request.method == 'POST':
        # Oturumdaki kullanıcıyı kontrol et
        kullanici_id = request.session.get('kullanici_id')

        if not kullanici_id:
            return HttpResponseBadRequest("Lütfen giriş yapın.")
        
      
        etkinlik_adi = request.POST.get('etkinlik_adi')
        aciklama = request.POST.get('aciklama')
        tarih = request.POST.get('tarih')
        saat = request.POST.get('saat')
        sure = request.POST.get('sure')
        kategori = request.POST.get('kategori')
        konum = request.POST.get('konum')

        # Süreyi 'HH:MM:SS' formatından dakika cinsine çevirme
        try:
            sure = int(sure)
        except ValueError:
            return HttpResponseBadRequest("Süre formatı hatalı, lütfen geçerli bir sayı giriniz.")

        # Adresi koordinatlara çevir
        geolocator = Nominatim(user_agent="myApp")
        location = geolocator.geocode(konum)

        if location:
            konum_latitude = location.latitude
            konum_longitude = location.longitude
        else:
            return HttpResponseBadRequest("Geçersiz adres, koordinatlar bulunamadı.")

        # Kullanıcı ID'si 1 ise etkinliği Etkinlik modeline kaydet
        if kullanici_id == 1:
            etkinlik = Etkinlik.objects.create(
                
                kullanici_id=1,
                etkinlik_adi=etkinlik_adi,
                aciklama=aciklama,
                tarih=tarih,
                saat=saat,
                sure=sure,
                kategori=kategori,
                konum=konum,
                konum_latitude=konum_latitude,
                konum_longitude=konum_longitude,
            )
            return redirect('anasayfa')

        # Kullanıcı ID'si 1 değilse, etkinliği onay_bekleyen_etkinlikler modeline kaydet
        else:
            # Burada 'onay_bekleyen_etkinlikler' modelini kullanmanız gerekebilir.
            # Örneğin:
            onay_bekleyen_etkinlik = OnayBekleyenEtkinlikler.objects.create(
                etkinlik_adi=etkinlik_adi,
                aciklama=aciklama,
                tarih=tarih,
                saat=saat,
                sure=sure,
                kategori=kategori,
                konum=konum,
                konum_latitude=konum_latitude,
                konum_longitude=konum_longitude,
                kullanici_id=kullanici_id  # Etkinliği oluşturan kullanıcıyı da kaydediyoruz
            )

            return redirect('anasayfa')

    return render(request, 'etkinlik_olustur.html')




def etkinlik_onayla(request):
    if request.method == 'POST':
            etkinlik_istek = request.session.get('etkinlik_istek')

            if etkinlik_istek:
                # Onaylanan etkinliği veritabanına kaydet
                etkinlik = Etkinlik.objects.create(
                    etkinlik_adi=etkinlik_istek['etkinlik_adi'],
                    aciklama=etkinlik_istek['aciklama'],
                    tarih=etkinlik_istek['tarih'],
                    saat=etkinlik_istek['saat'],
                    sure=etkinlik_istek['sure'],
                    kategori=etkinlik_istek['kategori'],
                    konum=etkinlik_istek['konum'],
                    konum_latitude=etkinlik_istek['konum_latitude'],
                    konum_longitude=etkinlik_istek['konum_longitude'],
                   
                )

                # Etkinlik isteğini temizle
                del request.session['etkinlik_istek']

                return JsonResponse({
                    'success': True,
                    'message': 'Etkinlik başarıyla onaylanıp kaydedildi.'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Onaylanacak etkinlik bulunamadı.'
                })
       






from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import Kullanici  # Kullanici modelinizi içe aktarın

def kullanici_giris(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            # Kullanıcıyı veritabanında bul
            kullanici = Kullanici.objects.get(kullanici_adi=username)
            
            # Şifreyi kontrol et
            if check_password(password, kullanici.sifre):
                # Giriş başarılı, kullanıcıyı oturum açtır
                request.session['kullanici_id'] = kullanici.id  # Kullanıcı ID'sini session'a kaydet
                print(f"Giriş yapan kullanıcının ID'si: {kullanici.id}")
                return redirect('anasayfa')  # Başarılı giriş sonrası 'arayuz' sayfasına yönlendir
            else:
                return render(request, 'login.html', {'error': 'Geçersiz şifre.'})
        except Kullanici.DoesNotExist:
            return render(request, 'login.html', {'error': 'Geçersiz kullanıcı adı.'})
    
    return render(request, 'login.html')




from django.shortcuts import render
from .models import Etkinlik
def anasayfa(request):
    
    user_id = request.session.get('kullanici_id', None)
    etkinlikler = Etkinlik.objects.all()  # Tüm etkinlikleri al
    return render(request, 'anasayfa.html', {'etkinlikler': etkinlikler,'user_id': user_id})




from datetime import  datetime, timedelta
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User  # Eğer User modelini kullanıyorsanız
from .models import Katilimci, Etkinlik, Kullanici  # Kullanici ve Katilimci modellerini import et
def katil(request, etkinlik_id):
    # Oturum açmış kullanıcının ID'sini session'dan al
    kullanici_id = request.session.get('kullanici_id')
    
    if not kullanici_id:
        # Eğer oturum açan kullanıcı yoksa, login sayfasına yönlendir
        return redirect('kullanici_giris')
    
    try:
        # Kullanıcıyı veritabanından al
        kullanici = Kullanici.objects.get(id=kullanici_id)
    except Kullanici.DoesNotExist:
        # Eğer kullanıcı bulunamazsa, hata sayfasına yönlendir veya hata mesajı göster
        return JsonResponse({'success': False, 'message': 'Kullanıcı bulunamadı!'})

    # Katılmak istenen etkinliği al
    try:
        yeni_etkinlik = Etkinlik.objects.get(id=etkinlik_id)
    except Etkinlik.DoesNotExist:
        # Eğer etkinlik bulunamazsa, hata mesajı göster
        return JsonResponse({'success': False, 'message': 'Etkinlik bulunamadı!'})

    # Kullanıcının mevcut etkinliklerini al
    mevcut_etkinlikler = Katilimci.objects.filter(kullanici=kullanici).select_related('etkinlik')

    # Yeni etkinliğin başlangıç ve bitiş zamanlarını belirle
    yeni_baslangic = datetime.combine(yeni_etkinlik.tarih, yeni_etkinlik.saat)
    yeni_bitis = yeni_baslangic + timedelta(minutes=yeni_etkinlik.sure)

    # Zaman çakışması kontrolü
    for katilim in mevcut_etkinlikler:
        mevcut_etkinlik = katilim.etkinlik
        mevcut_baslangic = datetime.combine(mevcut_etkinlik.tarih, mevcut_etkinlik.saat)
        mevcut_bitis = mevcut_baslangic + timedelta(minutes=mevcut_etkinlik.sure)

        # Çakışma varsa bilgilendirme
        if (yeni_baslangic < mevcut_bitis and yeni_bitis > mevcut_baslangic):
            return JsonResponse({
                'success': False,
                'message': f"Zaman çakışması: {mevcut_etkinlik.etkinlik_adi} etkinliğiyle çakışıyor."
            })
             # Çakışma varsa bilgilendirme
        if (mevcut_baslangic<yeni_bitis and mevcut_bitis>yeni_baslangic):
            return JsonResponse({
                'success': False,
                'message': f"Zaman çakışması: {mevcut_etkinlik.etkinlik_adi} etkinliğiyle çakışıyor."
            })

    # Eğer çakışma yoksa katılım kaydını oluştur
    katilimci, created = Katilimci.objects.get_or_create(kullanici=kullanici, etkinlik=yeni_etkinlik)

    # Başarılı işlem sonrası JSON yanıtı döndür
    if created:
        return JsonResponse({'success': True, 'message': 'Etkinliğe başarıyla katıldınız!'})
    else:
        return JsonResponse({'success': False, 'message': 'Zaten bu etkinliğe katılmışsınız!'})





from django.shortcuts import render, redirect
from .models import Kullanici

def profilim(request):
    # Kullanıcıyı session üzerinden al
    kullanici_id = request.session.get('kullanici_id')

    if not kullanici_id:
        # Eğer oturum açan kullanıcı yoksa, login sayfasına yönlendir
        return redirect('kullanici_giris')

    try:
        # Kullanıcıyı veritabanından al
        kullanici = Kullanici.objects.get(id=kullanici_id)
    except Kullanici.DoesNotExist:
        # Eğer kullanıcı bulunamazsa, hata sayfasına yönlendir veya hata mesajı göster
        return redirect('kullanici_giris')

    # Kullanıcının ilgi alanlarını al (session'dan ya da veritabanından)
    kullanici_ilgi_alanlari = request.session.get('ilgi_alanlari', None)

    # Eğer ilgi alanları session'da yoksa, veritabanındaki kullanıcıdan al
    if not kullanici_ilgi_alanlari:
        kullanici_ilgi_alanlari = kullanici.ilgi_alanlari or ""

    # İlgi alanlarını virgülle ayırıp listeye çevir
    ilgi_alanlari_listesi = [ilgi.strip().lower() for ilgi in kullanici_ilgi_alanlari.split(',') if ilgi.strip()]

    # İlgi alanlarına uygun etkinlikleri filtrele
    if ilgi_alanlari_listesi:
        uygun_etkinlikler = Etkinlik.objects.filter(kategori__in=ilgi_alanlari_listesi)
    else:
        uygun_etkinlikler = Etkinlik.objects.none()
  # Kullanıcının katıldığı etkinlikleri alıyoruz
    katilimlar = Katilimci.objects.filter(kullanici_id=kullanici_id)

    # Katıldığı etkinliklerin listesi
    etkinlikler = [katilim.etkinlik for katilim in katilimlar]

    # Kullanıcının toplam puanını hesaplıyoruz
    toplam_puan = 0
    katilimlar_count = len(katilimlar)
    etkinlik_olusturma_count =0

    # Katılım puanları (10 puan her etkinlik için)
    toplam_puan += katilimlar_count * 10

    # Etkinlik oluşturma puanları (15 puan her etkinlik oluşturma için)
    toplam_puan += etkinlik_olusturma_count + 15

    # İlk katılım bonusu (20 puan)
    if katilimlar_count > 0:
        toplam_puan += 20

    # Bugünün tarihini alıyoruz
    bugun = timezone.now().date()

    # Kullanıcının mevcut puan kaydını buluyoruz veya yeni bir kayıt oluşturuyoruz
    puan, created = Puan.objects.get_or_create(
        kullanici_id=kullanici_id,
        kazanilan_tarih=bugun,  # Bugünün tarihiyle
        defaults={'puan': 0}  # Eğer kayıt yoksa, puanı 0 olarak başlatıyoruz
    )

    # Puanı güncelliyoruz
    puan.puan = toplam_puan
    puan.save()
    # Etkinliklerin listesini ve kullanıcıyı şablona gönder
    return render(request, 'profilim.html', {
        'kullanici': kullanici,
          'toplam_puan': toplam_puan,
        'uygun_etkinlikler': uygun_etkinlikler
    })





from django.shortcuts import render, redirect
from .forms import ProfilGuncelleForm
from .models import Kullanici

def profil_guncelle(request):
    # Session'dan kullanıcı ID'sini alıyoruz
    kullanici_id = request.session.get('kullanici_id')
    
    if not kullanici_id:
        return redirect('login')  # Eğer session'da kullanıcı ID'si yoksa, giriş sayfasına yönlendir
    
    # Kullanıcıyı veritabanından alıyoruz
    kullanici = Kullanici.objects.get(id=kullanici_id)
    
    if request.method == 'POST':
        form = ProfilGuncelleForm(request.POST, request.FILES, instance=kullanici)
        if form.is_valid():
            form.save()  # Veritabanındaki kullanıcıyı güncelliyoruz
            return redirect('profilim')  # Profil sayfasına yönlendiriyoruz
    else:
        form = ProfilGuncelleForm(instance=kullanici)

    return render(request, 'profil_guncelle.html', {'form': form})




from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from .models import Kullanici

def sifremi_unuttum(request):
    if request.method == 'POST':
        email = request.POST['email']
        new_password = request.POST['new_password']

        try:
            # Kullanıcıyı e-posta adresine göre bul
            kullanici = Kullanici.objects.get(email=email)

            # Yeni şifreyi hashle
            kullanici.sifre = make_password(new_password)
            kullanici.save()

            # Başarı mesajı
            return render(request, 'sifre_sifirlama.html', {'success': 'Şifreniz başarıyla güncellenmiştir.'})
        except Kullanici.DoesNotExist:
            return render(request, 'sifre_sifirlama.html', {'error': 'Bu e-posta adresine kayıtlı bir kullanıcı bulunamadı.'})

    return render(request, 'sifre_sifirlama.html')



from .models import Katilimci, Etkinlik, Puan
from django.shortcuts import render, redirect
from django.utils import timezone

def katilan_etkinlikler(request):
    # Oturumdaki kullanıcı ID'sini alıyoruz
    kullanici_id = request.session.get('kullanici_id')  # Oturumdan kullanıcı ID'sini al

    if kullanici_id is None:
        return redirect('login')  # Eğer kullanıcı giriş yapmamışsa, login sayfasına yönlendir

    # Kullanıcının katıldığı etkinlikleri alıyoruz
    katilimlar = Katilimci.objects.filter(kullanici_id=kullanici_id)

    # Katıldığı etkinliklerin listesi
    etkinlikler = [katilim.etkinlik for katilim in katilimlar]

    # Kullanıcının toplam puanını hesaplıyoruz
    toplam_puan = 0
    katilimlar_count = len(katilimlar)
    etkinlik_olusturma_count = 0

    # Katılım puanları (10 puan her etkinlik için)
    toplam_puan += katilimlar_count * 10

    # Etkinlik oluşturma puanları (15 puan her etkinlik oluşturma için)
    toplam_puan += etkinlik_olusturma_count + 15

    # İlk katılım bonusu (20 puan)
    if katilimlar_count > 0:
        toplam_puan += 20

    # Bugünün tarihini alıyoruz
    bugun = timezone.now().date()

    # Kullanıcının mevcut puan kaydını buluyoruz veya yeni bir kayıt oluşturuyoruz
    puan, created = Puan.objects.get_or_create(
        kullanici_id=kullanici_id,
        kazanilan_tarih=bugun,  # Bugünün tarihiyle
        defaults={'puan': 0}  # Eğer kayıt yoksa, puanı 0 olarak başlatıyoruz
    )

    # Puanı güncelliyoruz
    puan.puan = toplam_puan
    puan.save()

    # Kullanıcının toplam puanını template'e gönderiyoruz
    return render(request, 'katilan_etkinlikler.html', {
        'etkinlikler': etkinlikler,
        'toplam_puan': toplam_puan
    })
    
    


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Etkinlik, Mesaj, Katilimci
from django.utils import timezone

def mesajlar(request, etkinlik_id):
    # Oturum açmış kullanıcının ID'sini session'dan al
    kullanici_id = request.session.get('kullanici_id')

    if not kullanici_id:
        # Eğer oturum açan kullanıcı yoksa, login sayfasına yönlendir
        return redirect('kullanici_giris')

    try:
        # Kullanıcıyı veritabanından al
        kullanici = Kullanici.objects.get(id=kullanici_id)
    except Kullanici.DoesNotExist:
        # Eğer kullanıcı bulunamazsa, hata sayfasına yönlendir veya hata mesajı göster
        return HttpResponseForbidden("Kullanıcı bulunamadı!")

    # Etkinliği ve o etkinliğe ait mesajları al
    etkinlik = get_object_or_404(Etkinlik, id=etkinlik_id)

    # Eğer kullanıcı etkinlikte katılımcı değilse, erişimi reddet
    if not Katilimci.objects.filter(kullanici=kullanici, etkinlik=etkinlik).exists():
        return HttpResponseForbidden("Bu etkinliğe katılmadığınız için mesajları görüntüleyemezsiniz.")

    # Mesaj gönderme işlemi
    if request.method == 'POST':
        # Mesaj metnini al
        mesaj_metni = request.POST.get('message')

        if mesaj_metni:
            # Yeni mesaj oluştur
            mesaj = Mesaj.objects.create(
                gonderici=kullanici,
                alici=kullanici,  # Burada 'alici'yi istediğiniz gibi değiştirebilirsiniz, örneğin etkinliğe katılan diğer kullanıcılar
                mesaj_metni=mesaj_metni,
                gonderim_zamani=timezone.now(),
                etkinlik=etkinlik  # Etkinlikle ilişkilendir
            )
            # Mesaj başarıyla gönderildikten sonra, aynı sayfaya geri yönlendirme
            return redirect('mesajlar', etkinlik_id=etkinlik.id)

    # Etkinliğe ait mesajları al
    mesajlar = Mesaj.objects.filter(etkinlik=etkinlik).order_by('-gonderim_zamani')

    return render(request, 'mesajlar.html', {'etkinlik': etkinlik, 'mesajlar': mesajlar, 'kullanici': kullanici})

from django.http import JsonResponse
from .models import Etkinlik

def delete_event(request, event_id):
    if request.method == 'DELETE':  # İstek türünü kontrol et
        try:
            etkinlik = Etkinlik.objects.get(id=event_id)
            etkinlik.delete()
            return JsonResponse({'success': True, 'message': 'Etkinlik başarıyla silindi.'})
        except Etkinlik.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Etkinlik bulunamadı.'})
    return JsonResponse({'success': False, 'message': 'Geçersiz istek türü.'})




from django.shortcuts import render, get_object_or_404, redirect
from .models import Etkinlik

def update_event(request, event_id):
    etkinlik = get_object_or_404(Etkinlik, id=event_id)
    if request.method == 'POST':
        # Formdan gelen verileri alıyoruz ve etkinlik objesini güncelliyoruz
        etkinlik.etkinlik_adi = request.POST['etkinlik_adi']
        etkinlik.aciklama = request.POST['aciklama']
        etkinlik.tarih = request.POST['tarih']
        etkinlik.saat = request.POST['saat']
        etkinlik.konum = request.POST['konum']
        etkinlik.save()
        
        # Güncellenmiş etkinliği detay sayfasına yönlendiriyoruz
        return redirect('anasayfa')

    # GET isteği ile formu kullanıcıya gösteriyoruz
    return render(request, 'update_event.html', {'etkinlik': etkinlik})



from django.shortcuts import render, redirect
from .models import Kullanici, Etkinlik

def etkinlik_oner(request):
    # Oturum açmış kullanıcının ID'sini session'dan al
    kullanici_id = request.session.get('kullanici_id')
    
    if not kullanici_id:
        # Eğer oturum açan kullanıcı yoksa, login sayfasına yönlendir
        return redirect('kullanici_giris')
    
    try:
        # Kullanıcıyı veritabanından al
        kullanici = Kullanici.objects.get(id=kullanici_id)
    except Kullanici.DoesNotExist:
        # Eğer kullanıcı bulunamazsa, hata sayfasına yönlendir
        return redirect('kullanici_giris')
    
    # Kullanıcının ilgi alanlarını al (CSV formatında, split ile ayırıyoruz)
    ilgi_alanlari = set(kullanici.ilgi_alanlari.split(','))
    
    # Etkinlikleri kullanıcının ilgi alanlarına göre filtreliyoruz
    etkinlikler = Etkinlik.objects.filter(kategori__in=ilgi_alanlari)
    
    return render(request, 'profilim.html', {'kullanici': kullanici, 'etkinlikler': etkinlikler})

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Kullanici, OnayBekleyenEtkinlikler, Etkinlik  # OnayBekleyenEtkinlikler ve Etkinlik modellerini içe aktar

def yonetim(request):
    # Kullanıcı ID'sini session'dan alıyoruz
    kullanici_id = request.session.get('kullanici_id')
    
    if not kullanici_id:
        # Eğer oturum açmamışsa giriş sayfasına yönlendir
        return redirect('kullanici_giris')

    if kullanici_id != 1:
        # Eğer ID 1 değilse yetkisiz erişim
        return HttpResponseForbidden("Bu sayfaya erişim yetkiniz yok.")

    # Tüm kullanıcıları listelemek için Kullanici modelini sorguluyoruz
    kullanicilar = Kullanici.objects.all().order_by('-date_joined')  # Kullanıcıları kayıt tarihine göre sıralıyoruz
    
    # Onay bekleyen etkinlikleri alıyoruz
    etkinlik_istekler = OnayBekleyenEtkinlikler.objects.filter(onaylanmis=False)  # onaylanmamış etkinlikleri al

    return render(request, 'yonetim.html', {
        'kullanicilar': kullanicilar,
        'etkinlik_istek': etkinlik_istekler  # Etkinlik taleplerini template'e gönderiyoruz
    })


def etkinlik_onayla(request, etkinlik_id):
    # Onay bekleyen etkinliği bul
    etkinlik = get_object_or_404(OnayBekleyenEtkinlikler, id=etkinlik_id)

    # Yeni etkinlik oluştur ve OnayBekleyenEtkinlikler'den al
    yeni_etkinlik = Etkinlik(
        id=etkinlik.id,  # Aynı ID'yi kullanıyoruz
        kullanici_id=etkinlik.kullanici_id,  # Kullanıcı ID'yi aynı bırakıyoruz
        etkinlik_adi=etkinlik.etkinlik_adi,
        aciklama=etkinlik.aciklama,
        tarih=etkinlik.tarih,
        saat=etkinlik.saat,
        kategori=etkinlik.kategori,
        konum=etkinlik.konum,
        konum_latitude=etkinlik.konum_latitude,
        konum_longitude=etkinlik.konum_longitude,
        sure=etkinlik.sure
    )
    yeni_etkinlik.save()

    # OnayBekleyenEtkinlikler tablosundan sil
    etkinlik.delete()

    # Yönetim paneline geri dön
    return redirect('yonetim')


from django.shortcuts import render, get_object_or_404, redirect
from .models import OnayBekleyenEtkinlikler

def etkinlik_duzenle(request, etkinlik_id):
    # OnayBekleyenEtkinlikler tablosundan etkinliği al
    etkinlik = get_object_or_404(OnayBekleyenEtkinlikler, id=etkinlik_id)

    if request.method == 'POST':
        # Formdan gelen verileri al
        etkinlik.etkinlik_adi = request.POST.get('etkinlik_adi')
        etkinlik.aciklama = request.POST.get('aciklama')
        etkinlik.tarih = request.POST.get('tarih')
        etkinlik.saat = request.POST.get('saat')
        etkinlik.kategori = request.POST.get('kategori')
        etkinlik.konum = request.POST.get('konum')
        etkinlik.konum_latitude = request.POST.get('konum_latitude')
        etkinlik.konum_longitude = request.POST.get('konum_longitude')
        etkinlik.sure = request.POST.get('sure')

        # Değişiklikleri kaydet
        etkinlik.save()

        # Düzenleme işleminden sonra yönlendirme
        return redirect('yonetim')  # Burada 'onaybekleyen_etkinlikler' yönlendirme URL'ini kullanıyoruz

    return render(request, 'etkinlik_duzenle.html', {'etkinlik': etkinlik})

 
 
from django.shortcuts import render
from .models import OnayBekleyenEtkinlikler

def etkinlikler_onaybekleyen(request):
    # Onay bekleyen etkinlikleri çek
    etkinlik_istek = OnayBekleyenEtkinlikler.objects.filter(onaylanmis=False)
    
    # Verileri şablona gönder
    return render(request, 'Yönetim.html', {'etkinlik_istek': etkinlik_istek})


from django.shortcuts import render

def etkinlik_detay(request, id):
    # Burada etkinlik verilerini alabilir ve template'e gönderebilirsiniz
    etkinlik = Etkinlik.objects.get(id=id)
    return render(request, 'etkinlik_detay.html', {'etkinlik': etkinlik})


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

def kullanici_sil(request, kullanici_id):
    # Kullanıcı ID'sini session'dan alıyoruz
    session_kullanici_id = request.session.get('kullanici_id')
    
    if not session_kullanici_id or session_kullanici_id != 1:
        # Eğer giriş yapmamışsa veya yetkisi yoksa
        return HttpResponseForbidden("Bu işlem için yetkiniz yok.")
    
    # Kullanıcıyı veritabanından bul ve sil
    kullanici = get_object_or_404(Kullanici, id=kullanici_id)
    kullanici.delete()
    
    # Silme işleminden sonra yönetim sayfasına yönlendir
    return HttpResponseRedirect(reverse('yonetim'))



from django.contrib.auth import logout
from django.shortcuts import redirect

def cikis(request):
    logout(request)  # Kullanıcıyı oturumdan çıkarır
    return redirect('kullanici_giris')  # Çıkış sonrası yönlendirme