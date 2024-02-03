from django.shortcuts import render
from django.views import View
from main._decorators import *
from main.models import *
from main.help import accommadationInfo
# Create your views here.




class HomeViewStudent(View):
    # @deco_login
    # @deco_url_student
    def get(self, request):
        
        all_dormitory = Accommadation.objects.all().count()
        rooms = Room.objects.all().count()
        students = Student.objects.filter(is_student=True)
        beds = Bed.objects.filter(status=False).count()
        students = students.count()    
        
        
        context = {
            "all_dormitory":all_dormitory,
            "rooms":rooms,
            "students":students,
            "beds":beds,

        }  
        
        return render(request,'student-pages/index-student.html',context)
    
    
class DormitoryStudentView(View):
    
    # @deco_login
    # @deco_url_student
    def get(self, request):
        accommadations = Accommadation.objects.all()
        beds = Bed.objects.all()
        context = accommadationInfo(accommadations,beds)
        
        context['accommadations'] = accommadations
      

        return render(request,'student-pages/info-dorm.html',context)
    

class StudentProfil(View):  
    def get(self,request):
        return render(request, 'student-pages/student-profil.html')