from django.urls import path
from .views import *
from .ajax import SearchStudent, GetPaymentInfo,ApplicationLoginView

app_name = 'main'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', logOut, name='logout'),
    
   
    
    path('', HomeView.as_view(), name='home'),
    path('students', StudentListView.as_view(), name='students'),
    path('control/dorm', ControlDorm.as_view(), name='control-dorm'),
    path('dormitory', DormitoryView.as_view(), name='dormitory'),
    path('price', MonthlyPaymentPriceView.as_view(), name='price-month'),
    path('price/edit/<int:pk>', MonthlyPaymentPriceView.as_view(), name='price-month-edit'),
    
    path('control/floor/<int:pk>', ControlFloor.as_view(), name='control-floor'),
    
    
    path('control/room/<int:pk>', ControlRoom.as_view(), name='control-room'),
    path('room/create/<int:pk>',ControlRoom.as_view(), name='create-room'),
    path('room/delete/<int:pk>',deleteRoom, name='delete-room'),
    path('room/update/<int:pk>',updateRoom, name='update-room'),
    
    
    path('control/bed/<int:pk>', ControlBed.as_view(), name='control-bed'),
    path('bed/create/<int:pk>',ControlBed.as_view(), name='create-bed'),
    path('bed/update/<int:pk>',updateBed, name='update-bed'),
    path('bed/delete/<int:pk>',deleteBed, name='delete-bed'),
    
    path('connect/student',StudentToBedView.as_view(), name='connect-create'),
    path('delete/student',delete_student_bed_view, name='connect-delete'),
    path('add/payment',AddPaymentView.as_view(), name='add-payment'),
    
    
    # ajax
    path('search/student', SearchStudent.as_view(), name='search-student'),
    path('get/payment/info', GetPaymentInfo.as_view(), name='get-payment'),
    path('application/login', ApplicationLoginView.as_view(), name='application-login'),

]
