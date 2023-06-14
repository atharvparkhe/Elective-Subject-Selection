from django.urls import path
from . import views


urlpatterns = [
	# Main
	path('', views.homePage, name="index"),
	path('time-table/', views.timeTable, name="time-table"),
	path('contact-us/', views.contactPage, name="contact-us"),

	# Subjects
	path('all-subjects/', views.allSubjects, name="all-subjects"),
	path('subject/<sub_id>/', views.singleSubject, name="single-subject"),

	# Dashboard
	path('student-dashboard/', views.StudentDashboard, name="student-dashboard"),
	# path('teacher-dashboard/', views.TeacherDashboard, name="teacher-dashboard"),
	# path('admin-dashboard/', views.AdminDashboard, name="admin-dashboard"),

	# Course Enrollment
	path('enroll/<num>/', views.enroll, name="enroll"),
	path('request-change-elective/<num>/', views.changeElective, name="change-elective"),
]