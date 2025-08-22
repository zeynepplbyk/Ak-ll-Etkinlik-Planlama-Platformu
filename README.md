# 🎯 Akıllı Etkinlik Planlama Platformu




## 📌 Proje Özeti
Bu proje kapsamında **web programlama bilgisi ve becerilerinin geliştirilmesi** hedeflenmiştir.  
- Web sayfası oluşturma  
- Veritabanı tasarımı ve yönetimi  
- Dinamik içerik geliştirme  
- Gerçek zamanlı veri işleme  
- Kullanıcı etkileşimi  
- Kural tabanlı kişiselleştirilmiş öneriler  

gibi yetkinlikler kazanılmıştır.  

Proje; **API entegrasyonları, harita ve rota planlama** özellikleriyle kullanıcı deneyimini zenginleştirmekte, ekip çalışması ile teknik zorlukların üstesinden gelinmiştir.  

---

## 🚀 Özellikler
- 📅 **Etkinlik Yönetimi**: Etkinlik oluşturma, katılma ve düzenleme  
- 🧑‍🤝‍🧑 **Sosyal Etkileşim**: Etkinliklere özel sohbet ve mesajlaşma alanı  
- 🗺️ **Harita Entegrasyonu**: Google Maps API ile etkinlik konumları ve rota planlama  
- 🤖 **Akıllı Öneri Sistemi**: İlgi alanı, geçmiş ve konuma göre kişiselleştirilmiş öneriler  
- ⏰ **Zaman Çakışma Algoritması**: Tarih/saat çakışmalarını engelleme  
- 🏆 **Oyunlaştırma**: Katılım ve etkinlik oluşturma üzerinden puan kazanma  
- 🔑 **Admin Paneli**: Kullanıcı ve etkinlik yönetimi  

---



## 🛠️ Kullanılan Teknolojiler
- **Backend**: [Django](https://www.djangoproject.com/) (Python)  
- **Frontend**: HTML, CSS, JavaScript  
- **Veritabanı**: Django ORM (SQLite)  
- **API**: Google Maps API  

---

## 📊 Sistem Modülleri
1. **Frontend Geliştirme** – HTML, CSS, JS ile kullanıcı arayüzü  
2. **Backend Geliştirme** – Django ile kullanıcı ve etkinlik yönetimi  
3. **Akıllı Öneri Sistemi** – Kural tabanlı algoritmalar  
4. **Harita & Rota Planlama** – Google Maps API  
5. **Mesajlaşma Sistemi** – Etkinlik bazlı sohbet odaları  
6. **Oyunlaştırma** – Katılım puanları  
7. **Admin Paneli** – Yönetici kontrolü  

---

## 📂 Veritabanı Yapısı
- **Kullanıcılar**: Kullanıcı adı, şifre, e-posta, profil bilgileri  
- **Etkinlikler**: İsim, açıklama, tarih, saat, konum  
- **Katılımcılar**: Kullanıcıların etkinliklerle ilişkisi  
- **Mesajlar**: Sohbet içerikleri  
- **Puanlar**: Oyunlaştırma için kullanıcı puanları  


<video width="600" controls>
  <source src="https://github.com/zeynepplbyk/Smart-Event-Planning-Platform-Akilli-Etkinlik-Planlama-Platformu/raw/main/kurulum.mp4" type="video/mp4">
  Tarayıcınız video oynatmayı desteklemiyor.
</video>


---

## ⚙️ Kurulum ve Çalıştırma
```bash

# Repoyu klonlayın
git clone https://github.com/zeynepplbyk/Smart-Event-Planning-Platform-Akilli-Etkinlik-Planlama-Platformu.git


# Proje dizinine gir
cd Smart-Event-Planning-Platform-Akilli-Etkinlik-Planlama-Platformu

# Sanal ortam oluştur ve etkinleştir
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt

# Migrasyonları uygula
python manage.py migrate

# Sunucuyu çalıştır
python manage.py runserver

```bash






