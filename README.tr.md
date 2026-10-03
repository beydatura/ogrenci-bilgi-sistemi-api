# Öğrenci Bilgi Sistemi API

Django ve Django REST Framework (DRF) kullanılarak geliştirilmiş, bir üniversitenin öğrenci/öğretmen/ders/kayıt (enrollment) işlemlerini yöneten bir REST API projesi.

[🇬🇧 English](README.md) | 🇹🇷 Türkçe

## İçindekiler

- [Projenin Amacı](#projenin-amacı)
- [Kullanılan Teknolojiler](#kullanılan-teknolojiler)
- [Kurulum Adımları](#kurulum-adımları)
- [Projeyi Çalıştırma](#projeyi-çalıştırma)
- [Veritabanı Modelleri](#veritabanı-modelleri)
- [Model İlişkileri](#model-i̇lişkileri)
- [Endpoint Listesi](#endpoint-listesi)
- [Filtreleme, Arama, Sıralama, Sayfalama](#filtreleme-arama-sıralama-sayfalama)
- [Örnek Request'ler ve Response'lar](#örnek-requestler-ve-responselar)
- [Validation Kuralları](#validation-kuralları)
- [HTTP Status Kodları](#http-status-kodları)
- [API Testleri](#api-testleri)
- [Postman Collection](#postman-collection)

---

## Projenin Amacı

Bu proje, bir üniversitenin öğrenci bilgi sistemini temsil eden bir **REST API** sunar. Frontend (React, Vue, Angular, Android, iOS veya başka bir istemci) veritabanına doğrudan bağlanmaz; tüm işlemler bu API üzerinden HTTP istekleriyle gerçekleştirilir:

```
Frontend / Mobil Uygulama → HTTP Request → Django REST Framework API → Django ORM → Database
```

API; bölüm (Department), öğrenci (Student), öğretmen (Teacher), ders (Course) ve ders kaydı (Enrollment) varlıkları üzerinde standart CRUD (Create/Read/Update/Delete) işlemlerini, bunlara ek olarak filtreleme, arama, sıralama ve sayfalama özelliklerini destekler.

## Kullanılan Teknolojiler

- **Python 3**
- **Django** — web framework, ORM
- **Django REST Framework (DRF)** — API katmanı (serializer, view, router)
- **django-filter** — alan bazlı filtreleme
- **SQLite** — geliştirme veritabanı
- **Postman** — API test aracı

## Kurulum Adımları

```bash
# 1. Repoyu klonla
git clone <repo-url>
cd obs_project

# 2. Sanal ortam oluştur ve aktif et
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Bağımlılıkları yükle
pip install django djangorestframework django-filter

# 4. Migration'ları uygula
python manage.py migrate

# 5. Süper kullanıcı oluştur (admin paneline erişim için)
python manage.py createsuperuser
```

## Projeyi Çalıştırma

```bash
python manage.py runserver
```

- API kök adresi: `http://127.0.0.1:8000/api/`
- Admin paneli: `http://127.0.0.1:8000/admin/`

## Veritabanı Modelleri

### Department (Bölüm)
| Alan | Tip | Açıklama |
|---|---|---|
| id | Integer | Birincil anahtar |
| name | CharField | Bölüm adı |
| description | TextField | Bölüm açıklaması |
| created_at | DateTimeField | Oluşturulma tarihi (otomatik) |

### Student (Öğrenci)
| Alan | Tip | Açıklama |
|---|---|---|
| id | Integer | Birincil anahtar |
| first_name | CharField | Ad |
| last_name | CharField | Soyad |
| email | EmailField | E-posta |
| student_number | CharField | Öğrenci numarası (benzersiz) |
| enrollment_date | DateField | Kayıt tarihi (otomatik) |
| department | ForeignKey → Department | Bağlı olduğu bölüm |

### Teacher (Öğretmen)
| Alan | Tip | Açıklama |
|---|---|---|
| id | Integer | Birincil anahtar |
| first_name | CharField | Ad |
| last_name | CharField | Soyad |
| email | EmailField | E-posta |
| specialization | CharField | Uzmanlık alanı |
| department | ForeignKey → Department | Bağlı olduğu bölüm |

### Course (Ders)
| Alan | Tip | Açıklama |
|---|---|---|
| id | Integer | Birincil anahtar |
| name | CharField | Ders adı |
| code | CharField | Ders kodu (benzersiz) |
| credit | IntegerField | Kredi |
| department | ForeignKey → Department | Bağlı olduğu bölüm |
| teacher | ForeignKey → Teacher | Dersi veren öğretmen |

### Enrollment (Ders Kaydı)
| Alan | Tip | Açıklama |
|---|---|---|
| id | Integer | Birincil anahtar |
| student | ForeignKey → Student | Kayıt olan öğrenci |
| course | ForeignKey → Course | Kayıt olunan ders |
| enrollment_date | DateField | Kayıt tarihi (otomatik) |
| grade | FloatField | Not (0-100 arası, boş olabilir) |

`unique_together = ('student', 'course')` — aynı öğrenci aynı derse birden fazla kez kaydedilemez.

## Model İlişkileri

```
Department (1) ─── (N) Student
Department (1) ─── (N) Teacher
Department (1) ─── (N) Course
Teacher    (1) ─── (N) Course

Student (N) ─── (N) Course   [Enrollment ara modeli üzerinden]
```

- Bir bölümün birden fazla öğrencisi, öğretmeni ve dersi olabilir; her öğrenci/öğretmen/ders yalnızca bir bölüme bağlıdır.
- Bir öğretmen birden fazla ders verebilir; her ders yalnızca bir öğretmene bağlıdır.
- Bir öğrenci birden fazla derse kaydolabilir, bir ders birden fazla öğrenci tarafından alınabilir — bu çoka-çok ilişki, ekstra bilgi (not, kayıt tarihi) taşıdığı için `Enrollment` ara modeli üzerinden kurulmuştur.

## Endpoint Listesi

Her kaynak (Department, Student, Teacher, Course, Enrollment) için standart CRUD endpoint'leri:

| Method | Endpoint | Açıklama |
|---|---|---|
| GET | `/api/departments/` | Tüm bölümleri listele |
| POST | `/api/departments/` | Yeni bölüm oluştur |
| GET | `/api/departments/{id}/` | Tek bölümü görüntüle |
| PUT | `/api/departments/{id}/` | Bölümü tamamen güncelle |
| PATCH | `/api/departments/{id}/` | Bölümü kısmi güncelle |
| DELETE | `/api/departments/{id}/` | Bölümü sil |
| GET | `/api/students/` | Tüm öğrencileri listele |
| POST | `/api/students/` | Yeni öğrenci oluştur |
| GET | `/api/students/{id}/` | Tek öğrenciyi görüntüle |
| PUT | `/api/students/{id}/` | Öğrenciyi tamamen güncelle |
| PATCH | `/api/students/{id}/` | Öğrenciyi kısmi güncelle |
| DELETE | `/api/students/{id}/` | Öğrenciyi sil |
| GET | `/api/teachers/` | Tüm öğretmenleri listele |
| POST | `/api/teachers/` | Yeni öğretmen oluştur |
| GET | `/api/teachers/{id}/` | Tek öğretmeni görüntüle |
| PUT | `/api/teachers/{id}/` | Öğretmeni tamamen güncelle |
| PATCH | `/api/teachers/{id}/` | Öğretmeni kısmi güncelle |
| DELETE | `/api/teachers/{id}/` | Öğretmeni sil |
| GET | `/api/courses/` | Tüm dersleri listele |
| POST | `/api/courses/` | Yeni ders oluştur |
| GET | `/api/courses/{id}/` | Tek dersi görüntüle |
| PUT | `/api/courses/{id}/` | Dersi tamamen güncelle |
| PATCH | `/api/courses/{id}/` | Dersi kısmi güncelle |
| DELETE | `/api/courses/{id}/` | Dersi sil |
| GET | `/api/enrollments/` | Tüm ders kayıtlarını listele |
| POST | `/api/enrollments/` | Öğrenciyi derse kaydet |
| GET | `/api/enrollments/{id}/` | Tek kaydı görüntüle |
| PUT | `/api/enrollments/{id}/` | Kaydı tamamen güncelle |
| PATCH | `/api/enrollments/{id}/` | Kaydı kısmi güncelle |
| DELETE | `/api/enrollments/{id}/` | Kaydı sil |

## Filtreleme, Arama, Sıralama, Sayfalama

| Özellik | Örnek | Açıklama |
|---|---|---|
| Filtreleme | `GET /api/students/?department=1` | Belirli bir bölüme ait öğrencileri getirir |
| Filtreleme | `GET /api/courses/?teacher=2` | Belirli bir öğretmenin derslerini getirir |
| Arama | `GET /api/students/?search=Ahmet` | Ad/soyad/email içinde arama yapar |
| Sıralama | `GET /api/students/?ordering=first_name` | Ada göre artan sıralar |
| Sıralama | `GET /api/students/?ordering=-enrollment_date` | Kayıt tarihine göre azalan sıralar |
| Sayfalama | `GET /api/students/?page=2` | İkinci sayfayı getirir (sayfa başına 5 kayıt) |

Tüm bu parametreler birlikte de kullanılabilir, örn: `GET /api/courses/?department=1&ordering=name&search=Python`

## Örnek Request'ler ve Response'lar

### Yeni öğrenci oluşturma

**Request:**
```
POST /api/students/
Content-Type: application/json

{
    "first_name": "Zeynep",
    "last_name": "Kaya",
    "email": "zeynep@example.com",
    "student_number": "20260099",
    "department": 1
}
```

**Response (201 Created):**
```json
{
    "id": 6,
    "first_name": "Zeynep",
    "last_name": "Kaya",
    "email": "zeynep@example.com",
    "student_number": "20260099",
    "enrollment_date": "2026-09-05",
    "department": 1
}
```

### Öğrenci detayını görüntüleme (ilişkili verilerle)

**Request:**
```
GET /api/students/1/
```

**Response (200 OK):**
```json
{
    "id": 1,
    "first_name": "Ali",
    "last_name": "Çelik",
    "email": "ali.celik@ogrenci.edu.tr",
    "student_number": "20260001",
    "enrollment_date": "2026-09-05",
    "department": {
        "id": 1,
        "name": "Bilgisayar Mühendisliği",
        "description": "",
        "created_at": "2026-09-05T15:04:53.920169Z"
    },
    "enrollments": [
        {
            "id": 1,
            "course": {
                "id": 1,
                "name": "Python Programlama",
                "code": "CENG101",
                "credit": 4
            },
            "enrollment_date": "2026-09-05",
            "grade": 85.5
        }
    ]
}
```

### Hatalı istek örneği (validation)

**Request:**
```
POST /api/students/
Content-Type: application/json

{
    "first_name": "",
    "student_number": "20260001",
    "department": 999
}
```

**Response (400 Bad Request):**
```json
{
    "first_name": ["This field may not be blank."],
    "email": ["This field is required."],
    "student_number": ["student with this student number already exists."],
    "department": ["Invalid pk \"999\" - object does not exist."]
}
```

### Bulunamayan kayıt örneği

**Request:**
```
GET /api/students/9999/
```

**Response (404 Not Found):**
```json
{
    "detail": "Not found."
}
```

## Validation Kuralları

- Ad/soyad alanları boş bırakılamaz
- E-posta geçerli formatta olmalıdır
- Öğrenci numarası ve ders kodu benzersiz olmalıdır
- Olmayan bir bölüme/öğretmene/öğrenciye/derse referans verilemez
- Aynı öğrenci aynı derse iki kez kaydedilemez
- Not (grade) değeri 0-100 aralığı dışında olamaz

## HTTP Status Kodları

| Kod | Kullanım |
|---|---|
| 200 OK | Başarılı GET, PUT, PATCH |
| 201 Created | Başarılı POST |
| 204 No Content | Başarılı DELETE |
| 400 Bad Request | Geçersiz/eksik veri |
| 404 Not Found | Kaynak bulunamadı |

## API Testleri

Tüm endpoint'ler Postman kullanılarak hem başarılı hem hatalı senaryolarla test edilmiştir:
- CRUD akışı (oluştur → listele → görüntüle → güncelle → sil)
- Benzersizlik ihlalleri (tekrar eden öğrenci numarası/ders kodu)
- Geçersiz ilişki referansları (olmayan bölüm/öğretmen/öğrenci/derse referans)
- Aralık dışı not girişi
- Aynı öğrenci-ders ikilisine tekrar kayıt denemesi
- Var olmayan kayıtlara erişim (404 senaryosu)
- Filtreleme, arama, sıralama ve sayfalama parametrelerinin kombinasyonları

## Postman Collection

Projenin tüm API endpoint'lerini içeren hazır bir Postman collection'ı
`postman/Öğrenci Bilgi Sistemi API.postman_collection.json` dosyasında bulunmaktadır.

### Nasıl kullanılır?
1. Postman'i aç
2. Sol üstten **Import** butonuna tıkla
3. `postman/Öğrenci Bilgi Sistemi API.postman_collection.json` dosyasını seç
4. Collection otomatik olarak tüm endpoint'lerle (Departments, Students, Teachers,
   Courses, Enrollments) birlikte yüklenecektir  