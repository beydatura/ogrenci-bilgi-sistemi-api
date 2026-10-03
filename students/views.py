from rest_framework import viewsets
from .models import Department, Student, Teacher, Course, Enrollment
from .serializers import (
    DepartmentSerializer,
    StudentSerializer, StudentDetailSerializer,
    TeacherSerializer,
    CourseSerializer, CourseDetailSerializer,
    EnrollmentSerializer,
)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    filterset_fields = ['department']
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'last_name', 'enrollment_date']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return StudentDetailSerializer
        return StudentSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filterset_fields = ['department']
    search_fields = ['first_name', 'last_name', 'email', 'specialization']
    ordering_fields = ['first_name', 'last_name']


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    filterset_fields = ['department', 'teacher']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'credit']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseDetailSerializer
        return CourseSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    filterset_fields = ['student', 'course']
    ordering_fields = ['enrollment_date', 'grade']