from django.db import models

# 1. BÖLÜM TABLOSU
class Department(models.Model): #Django'nun temel model özelliklerini miras aldığını ve SQL tablosuna dönüştürüleceğini belirtir.
    name = models.CharField(max_length=100)           # Bölüm adı (en fazla 100 karakter)
    description = models.TextField(blank=True)        # Uzun açıklama (admin panelinde bu alan boş bırakılabilir)
    created_at = models.DateTimeField(auto_now_add=True) # Eklenme tarih ve saatini otomatik kaydeder ve sonraki güncellemelerde bu değeri değiştirmez.

    def __str__(self):
        return self.name                              # Ekranda/Admin panelinde bölüm adını gösterir


# 2. ÖĞRENCİ TABLOSU
class Student(models.Model):
    first_name = models.CharField(max_length=50)      # Öğrencinin adı
    last_name = models.CharField(max_length=50)       # Öğrencinin soyadı
    email = models.EmailField()                       # Geçerli bir e-posta formatı zorunlu
    student_number = models.CharField(max_length=20, unique=True) # aynı öğrenci numarasından ikinci kaydın girilmesini engeller.
    enrollment_date = models.DateField(auto_now_add=True)         # Okula kayıt tarihini otomatik basar
    department = models.ForeignKey(                   # Öğrenciyi bir bölüme bağlar (1 Bölüm -> Çok Öğrenci)
        Department, 
        on_delete=models.CASCADE,                     # Bölüm silinirse o bölüme ait öğrenciler de silinir
        related_name='students'                       # Bölümden öğrencilere ulaşmak için ters bağlantı adı
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # Ekranda öğrencinin adını ve soyadını gösterir


# 3. ÖĞRETMEN TABLOSU
class Teacher(models.Model):
    first_name = models.CharField(max_length=50)      # Öğretmenin adı
    last_name = models.CharField(max_length=50)       # Öğretmenin soyadı
    email = models.EmailField()                       # E-posta adresi
    specialization = models.CharField(max_length=100) # Uzmanlık alanı (ör: Veri Tabanı, Yapay Zeka)
    department = models.ForeignKey(                   # Öğretmeni bir bölüme bağlar
        Department, 
        on_delete=models.CASCADE,                     # Bölüm silinirse öğretmen de silinir
        related_name='teachers'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # Ekranda öğretmenin adını ve soyadını gösterir


# 4. DERS TABLOSU
class Course(models.Model):
    name = models.CharField(max_length=100)           # Dersin adı
    code = models.CharField(max_length=20, unique=True) # Ders kodu (ör: PY101, benzersiz olmalı)
    credit = models.IntegerField()                    # Dersin kredi sayısı (tam sayı)
    department = models.ForeignKey(                   # Dersi açan bölüm
        Department, 
        on_delete=models.CASCADE, 
        related_name='courses'
    )
    teacher = models.ForeignKey(                      # Dersi veren öğretmen
        Teacher, 
        on_delete=models.CASCADE, 
        related_name='courses'
    )

    def __str__(self):
        return self.name                              # Ekranda dersin adını gösterir


# 5. DERS KAYIT TABLOSU (ARA TABLO)
class Enrollment(models.Model):
    student = models.ForeignKey(                      # Dersi alan öğrenci
        Student, 
        on_delete=models.CASCADE, 
        related_name='enrollments'
    )
    course = models.ForeignKey(                       # Alınan ders
        Course, 
        on_delete=models.CASCADE, 
        related_name='enrollments'
    )
    enrollment_date = models.DateField(auto_now_add=True) # Derse kayıt olma tarihi
    grade = models.FloatField(null=True, blank=True)      # Sınav notu (ilk başta boş kalabilir)

    class Meta:
        # Aynı öğrencinin aynı derse ikinci kez kayıt olmasını veritabanında engeller
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} - {self.course}"      # Ekranda "Öğrenci Adı - Ders Adı" gösterir