# Django REST Framework'ün serializer modülünü içeri aktarıyoruz
from rest_framework import serializers

# Dönüştürülecek veritabanı modellerini çağırıyoruz
from .models import Department, Student, Teacher, Course, Enrollment


# 1. BÖLÜM MODELİ SERIALIZER'I
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'  # Bölüme ait tüm sütunları JSON formatına çevirir


# 2. ÖĞRETMEN MODELİ SERIALIZER'I
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'  # Öğretmene ait tüm sütunları JSON formatına çevirir


# 3. ÖĞRENCİ EKLEME/GÜNCELLEME SERIALIZER'I (YAZMA İŞLEMİ)
class StudentSerializer(serializers.ModelSerializer):
    """Yazma (create/update) için kullanılır — department alanı ID kabul eder."""
    class Meta:
        model = Student
        # Yeni öğrenci kaydederken veya güncellerken doğrudan model alanlarını ve bölüm ID'sini doğrular
        fields = '__all__'


# 4. ÖZET DERS SERIALIZER'I (MİMARİDE YARDIMCI GÖSTERİM)
class CourseMiniSerializer(serializers.ModelSerializer):
    """Öğrenci detayında dersi kısa göstermek için."""
    class Meta:
        model = Course
        # İlişkili alt listelerde şişkinlik yaratmamak adına sadece temel ders bilgilerini döner
        fields = ['id', 'name', 'code', 'credit']


# 5. ÖZET ÖĞRENCİ SERIALIZER'I (MİMARİDE YARDIMCI GÖSTERİM)
class StudentMiniSerializer(serializers.ModelSerializer):
    """Ders detayında kayıtlı öğrenciyi kısa göstermek için."""
    class Meta:
        model = Student
        # Bir dersin altında listelenen kayıtlı öğrencilerin sadece temel kimlik bilgilerini verir
        fields = ['id', 'first_name', 'last_name', 'student_number']


# 6. DERS KAYDI VE NOT GİRİŞİ SERIALIZER'I (YAZMA İŞLEMİ)
class EnrollmentSerializer(serializers.ModelSerializer):
    """Yazma (create/update) için kullanılır — student ve course alanları ID kabul eder."""

    class Meta:
        model = Enrollment
        fields = '__all__'

    # Özel alan doğrulama (Validation): Not değerinin mantıksal sınırını kontrol eder
    def validate_grade(self, value):
        # Not girilmişse ve 0 ile 100 aralığında değilse API hata döndürür
        if value is not None and not (0 <= value <= 100):
            raise serializers.ValidationError("Not değeri 0 ile 100 arasında olmalıdır.")
        return value


# 7. ÖĞRENCİ DETAYINDA DERS LİSTESİ İÇİN SERIALIZER
class EnrollmentDetailSerializer(serializers.ModelSerializer):
    """Öğrenci detayında, öğrencinin aldığı dersleri göstermek için."""
    # course alanını sade bir ID yerine dersin adı ve kodunu içeren mini yapıya dönüştürür (salt okunur)
    course = CourseMiniSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'enrollment_date', 'grade']


# 8. ÖĞRENCİ DETAY GÖSTERİM SERIALIZER'I (OKUMA İŞLEMİ)
class StudentDetailSerializer(serializers.ModelSerializer):
    """Okuma (list/retrieve) için kullanılır — ilişkili veriler iç içe (nested) gösterilir."""
    # Bölüm ID'si yerine bölümün tüm detaylarını iç içe (nested) JSON nesnesi olarak ekler
    department = DepartmentSerializer(read_only=True)
    # Öğrencinin related_name='enrollments' üzerinden aldığı tüm ders kayıtlarını dizi halinde getirir
    enrollments = EnrollmentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'student_number', 'enrollment_date', 'department', 'enrollments',
        ]


# 9. DERS EKLEME/GÜNCELLEME SERIALIZER'I (YAZMA İŞLEMİ)
class CourseSerializer(serializers.ModelSerializer):
    """Yazma (create/update) için kullanılır — department ve teacher ID kabul eder."""
    class Meta:
        model = Course
        fields = '__all__'  # Yeni ders açarken department ve teacher alanlarına sadece ID verilmesini sağlar


# 10. DERS DETAY GÖSTERİM SERIALIZER'I (OKUMA İŞLEMİ)
class CourseDetailSerializer(serializers.ModelSerializer):
    """Okuma (list/retrieve) için kullanılır."""
    # Dersi açan bölümün ve dersi veren öğretmenin detaylı nesnelerini gösterir
    department = DepartmentSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    # Modelde doğrudan bulunmayan, aşağıdaki get_enrolled_students fonksiyonuyla hesaplanan özel alan
    enrolled_students = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'credit', 'department', 'teacher', 'enrolled_students']

    # Bu derse kayıtlı öğrencileri ve o dersteki notlarını toplayıp JSON listesi olarak hazırlar
    def get_enrolled_students(self, obj):
        enrollments = obj.enrollments.all()  # Derse ait bütün kayıt satırlarını çeker
        return [
            {'student': StudentMiniSerializer(e.student).data, 'grade': e.grade}
            for e in enrollments
        ]