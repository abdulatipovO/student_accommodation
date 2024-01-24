from django.urls import path
from .views import *


app_name = 'student'

urlpatterns = [
    path('home', HomeViewStudent.as_view(), name='student-home'),
    path('info/dorm', DormitoryStudentView.as_view(), name='info-dorm'),
    path('profil', StudentProfil.as_view(), name='profil'),
]