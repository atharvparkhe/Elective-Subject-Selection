from django.urls import path
from . import views


urlpatterns = [
    # Common
	path('mail-message/', views.mailMessage, name="mail-message"),
	path('logout/', views.logoutView, name="logout"),

    # Student Auth
	path('student-login/', views.StudentLogIn, name="student-login"),
	path('student-forgot/', views.StudentForgot, name="student-forgot"),
	path('student-reset/<token>/', views.StudentReset, name="student-reset"),
    # Teacher Auth
	path('teacher-login/', views.TeacherLogIn, name="teacher-login"),
	path('teacher-forgot/', views.TeacherForgot, name="teacher-forgot"),
	path('teacher-reset/<token>/', views.TeacherReset, name="teacher-reset"),
    # Admin Auth
	path('admin-login/', views.AdminLogIn, name="admin-login"),
	path('admin-forgot/', views.AdminForgot, name="admin-forgot"),
	path('admin-reset/<token>/', views.AdminReset, name="admin-reset"),
    
	# Teacher
	path('all-teachers/', views.allTeachers, name="all-teachers"),
	path('teacher/<teacher_id>/', views.singleTeacher, name="single-teacher"),
	path('add-teacher/', views.addTeacher, name="add-teacher"),
    
	# Student
	path('add-single-student/', views.addStudent, name="add-single-student"),
	path('add-multiple-students/', views.addMultipleStudents, name="add-multiple-students"),

]