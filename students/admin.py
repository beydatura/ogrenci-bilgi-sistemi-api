from django.contrib import admin
from .models import Department, Student, Teacher, Course, Enrollment

# modelleri admin paneline kaydediyoruz

admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Enrollment)