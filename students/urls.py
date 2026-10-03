# Django REST Framework'ün URL rotalarını otomatik üreten sınıfını içeri aktarıyoruz
from rest_framework.routers import DefaultRouter

# URL rotalarına bağlanacak olan ViewSet sınıflarını views.py dosyasından çekiyoruz
from .views import (
    DepartmentViewSet, 
    StudentViewSet, 
    TeacherViewSet,
    CourseViewSet, 
    EnrollmentViewSet,
)

# Rota yöneticisi (DefaultRouter) nesnesini ayağa kaldırıyoruz
# DefaultRouter; kök dizinde tüm API uçlarını gösteren interaktif bir ana sayfa da sunar
router = DefaultRouter()

# 1. Bölümler için URL'leri kaydet (/departments/ ve /departments/<id>/)
router.register('departments', DepartmentViewSet)

# 2. Öğrenciler için URL'leri kaydet (/students/ ve /students/<id>/)
router.register('students', StudentViewSet)

# 3. Öğretmenler için URL'leri kaydet (/teachers/ ve /teachers/<id>/)
router.register('teachers', TeacherViewSet)

# 4. Dersler için URL'leri kaydet (/courses/ ve /courses/<id>/)
router.register('courses', CourseViewSet)

# 5. Kayıtlar ve notlar için URL'leri kaydet (/enrollments/ ve /enrollments/<id>/)
router.register('enrollments', EnrollmentViewSet)

# Router tarafından arka planda otomatik üretilen tüm URL listesini Django'nun urlpatterns listesine atıyoruz
urlpatterns = router.urls