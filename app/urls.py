from django.urls import path
from . import views


urlpatterns = [
	# Landing Page
	path('', views.homePage, name="index"),
	# Subjects
	path('all-subjects', views.allSubjects, name="all-subjects"),
	path('subject/<sub_id>/', views.singleSubject, name="single-subject"),
    # 
]