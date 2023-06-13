from django.urls import path
from . import views


urlpatterns = [
	# Main
	path('', views.homePage, name="index"),
	path('time-table/', views.timeTable, name="time-table"),
	
	# Subjects
	path('all-subjects/', views.allSubjects, name="all-subjects"),
	path('subject/<sub_id>/', views.singleSubject, name="single-subject"),
    
	# 
]