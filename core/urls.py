# Django'nun dahili yönetim panelini içeri aktarıyoruz
from django.contrib import admin

# path (URL rotası tanımlamak) ve include (başka bir app'in URL'lerini projeye bağlamak) fonksiyonlarını içe aktarıyoruz
from django.urls import path, include
from django.views.generic import RedirectView

# Projenin ana rota haritası
urlpatterns = [
    # 1. Admin Paneli Rotası
    # http://127.0.0.1:8000/admin/ adresine gelen istekleri Django'nun hazır yönetim sistemine yönlendirir
    path('admin/', admin.site.urls),

    # 2. API Uç Noktaları Rotası
    # http://127.0.0.1:8000/api/ ile başlayan bütün istekleri students uygulamasının urls.py dosyasına devreder
    # Böylece students/urls.py içindeki rotalar http://127.0.0.1:8000/api/students/, http://127.0.0.1:8000/api/courses/ şeklinde çalışır
    path('api/', include('students.urls')),
    path('', RedirectView.as_view(url='/api/', permanent=False)),
]