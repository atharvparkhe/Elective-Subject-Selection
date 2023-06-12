from django.urls import path
from . import views


urlpatterns = [
    # Student
	path('student-login/', views.StudentLogIn, name="student-login"),
	path('student-forgot/', views.StudentForgot, name="student-forgot"),
	path('student-reset/', views.StudentReset, name="student-reset"),
    # Teacher
	path('teacher-login/', views.TeacherLogIn, name="teacher-login"),
	path('teacher-forgot/', views.TeacherForgot, name="teacher-forgot"),
	path('teacher-reset/', views.TeacherReset, name="teacher-reset"),
    # Admin
	path('admin-login/', views.AdminLogIn, name="admin-login"),
	path('admin-forgot/', views.AdminForgot, name="admin-forgot"),
	path('admin-reset/', views.AdminReset, name="admin-reset"),
]