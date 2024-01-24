from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ._decorators import deco_login, deco_url_admin
from .help import *

# Create your views here.


class MonthlyPaymentPriceView(View):
    def get(self,request):
        
        monthly_price = MonthlyPaymentPrice.objects.all()[0]
        
        context = {
            "monthly_price":monthly_price
        }
        
        return render(request,'monthy_payment_price.html',context)

    def post(self, request, pk):
        
        velue = int(request.POST['edit_price'])
        
        price = MonthlyPaymentPrice.objects.filter(id=int(pk))[0]
        price.price = velue
        
        price.save()
        return redirect('/price')

class HomeView(View):
    
    @deco_login
    @deco_url_admin
    def get(self, request):
        
        # Student.objects.create_user(
            
        #     student_id = "000000000000 ",
        #     first_name = "admin",
        #     last_name = "admin",
        #     middle_name = "admin",
        #     passport = "AV2767139",
        #     faculty = "admin",
        #     course_of_study = "admin",
        #     stage=4,
        #     group = "71",
        #     phone = "+998932525756",
        #     email = "admin123@mail.ru",
        #     username = "admin",
        #     password = "admin123",
        #     is_admin=True,
        #     gender="male"

        # )
        # print("create")
        
        all_dormitory = Accommadation.objects.all().count()
        rooms = Room.objects.all().count()
        students = Student.objects.filter(is_student=True)
        boys = students.filter(gender='male').all().count()  
        girls = students.filter(gender='female').count()  
        students = students.count()  
        applications = Application.objects.all()
        
        calc =  CalculationMoney()
        
        autumn_semester = calc[0]['payment_amount__sum']
        spring_semester = calc[1]['payment_amount__sum']
        
 
        context = {
            "all_dormitory":all_dormitory,
            "rooms":rooms,
            "students":students,
            "boys":boys,
            "girls":girls,
            "applications":applications,
            "autumn_semester":autumn_semester,
            "spring_semester":spring_semester,
            
        }  
        return render(request,'index.html', context)
    
    
class StudentListView(View):
    
    @deco_login
    @deco_url_admin
    def get(self, request):
        
        # beds = Bed.objects.select_related('room__floor__accommadation').all()
        
        students = Student.objects.filter(is_student=True)
        students = students.exclude(bed__isnull=True)
        
        print(students)
        
        context = {
            "students":students
        }
        
        return render(request,'students-datatable.html',context)
    
    
class DormitoryView(View):
    
    @deco_login
    @deco_url_admin
    def get(self, request):
        accommadations = Accommadation.objects.all()
        beds = Bed.objects.all()
        students = Student.objects.filter(is_student=True, bed=None)
        monthly_price = MonthlyPaymentPrice.objects.all()[0]
        
   
        context = accommadationInfo(accommadations,beds)
        
        context['accommadations'] = accommadations
        context['students'] = students
        context['monthly_price'] = monthly_price
            
    
        return render(request,'all-accommadation.html',context)
    
    
class ControlDorm(View):
    @deco_login
    @deco_url_admin
    def get(self, request):
        accommadations = Accommadation.objects.all()
        
        context = {
            "accommadations":accommadations
        }

        return render(request,'control-dorm.html',context)
    
    
    def post(self, request):
        dorm_title = request.POST['dorm_title']
        gender = request.POST['gender']
        
        Accommadation.objects.create(title=dorm_title, type=gender)
        messages.success(request, "Bino yaratildi")
        
        return redirect('/control/dorm')
    
    
class ControlFloor(View):
    def get(self, request,pk):
        
        accommadation = Accommadation.objects.filter(pk=pk)[0]
        floors = accommadation.accommadations.all()
        
        
        context = {
            "accommadation":accommadation,
            "floors":floors
        }

        return render(request,'control-floor.html',context)
    
    
    def post(self, request,pk):
        
        floor_title = request.POST['floor_title']
        
        Floor.objects.create(accommadation_id=int(pk),title=floor_title)
        messages.success(request, "Qavat yaratildi")
        
        return redirect(f'/control/floor/{pk}')
    
    
    
class ControlRoom(View):
    def get(self, request,pk):
        
        floor = Floor.objects.filter(pk=pk)[0]
        rooms = floor.floors.all()
        
        
        context = {
            "floor":floor,
            "rooms":rooms
        }

        return render(request,'control-room.html',context)
    
    def post(self, request,pk):
        title = request.POST['room_title']
        Room.objects.create(floor_id=int(pk), title=title)
        messages.success(request, "Xona yaratildi")
        
        return redirect(f'/control/room/{pk}')
    
    
def deleteRoom(request, pk):
    room_id = request.POST['room_id']
    room_id = Room.objects.get(id=int(room_id))
    room_id.delete()
    
    messages.success(request, "Xona o'chirib tashlandi !")
    
    return redirect(f'/control/room/{pk}')


def updateRoom(request, pk):
    room_id = request.POST['room_id']
    room_title = request.POST['room_title']
    
    room = Room.objects.get(id=int(room_id))
    room.title = room_title
    room.save()
    
    messages.success(request, "Xona raqami tahrirlandi !")
    
    return redirect(f'/control/room/{pk}')
    
   
    
    
class ControlBed(View):
    def get(self, request,pk):
        
        room = Room.objects.filter(pk=pk)[0]
        beds = room.rooms.all()
        
        students = Student.objects.filter(is_student=True, bed=None)
        
        context = {
            "room":room,
            "beds":beds,
            "students":students
        }

        return render(request,'control-bed.html',context)
    
    def post(self, request,pk):
        
        bed_number = request.POST['bed_number']
        
        Bed.objects.create(room_id=int(pk), bed_number=bed_number)
        
        messages.success(request, "Joy yaratildi")
        
        return redirect(f'/control/bed/{pk}')
    
def deleteBed(request, pk):
    
    bed_id = request.POST['bed_id']
    bed = Bed.objects.get(id=int(bed_id))
    bed.delete()
    
    messages.success(request, "Joy o'chirib tashlandi !")
    
    return redirect(f'/control/bed/{pk}')


def updateBed(request, pk):
    bed_id = request.POST['bed_id']
    bed_number = request.POST['bed_number']
    
    bed = Bed.objects.get(id=int(bed_id))
    bed.bed_number = bed_number
    bed.save()
    
    messages.success(request, "Joy raqami tahrirlandi !")
    
    return redirect(f'/control/bed/{pk}')
    
    
    
class StudentToBedView(View):
    
    def post(self, request):
       
        student_connect = studentConnectToBed(request)
        
        if student_connect is None:
            messages.error(request, "Talaba kiritishda xatolik !")
            return redirect('/dormitory')
        
        
        messages.success(request, "Talaba joyga biriktirildi!")
        return redirect('/dormitory')
    

def delete_student_bed_view(request):
    
    bed_id = request.POST['bed_id']
    student_id = request.POST['student_id']
    
    try:
        bed = Bed.objects.get(id=int(bed_id))
         
        student = Student.objects.get(id=int(student_id))
        
        paymentInfo = PaymentInfo.objects.filter(student_id=int(student.student_id))[0]
        
  
    except:
        bed =  None
        student =  None
        paymentInfo =  None
        
    
    
    if bed != None and student != None and paymentInfo != None:
        student.bed = None
        bed.status = False
        
        info_history = BedInfoHistory.objects.create(
            bed_id=int(bed.id),
            student_id=paymentInfo.student_id,
            start_date=paymentInfo.start_date,
            end_date=paymentInfo.end_date,
            payment_amount=paymentInfo.payment_amount,
            difference_money=paymentInfo.difference_money,
        )
        
        add_paymentInfoHistory = AddPaymentInfo.objects.filter(student_id=paymentInfo.student_id)
           
            
        for add_history in add_paymentInfoHistory:
            
            add_payment_info_history = AddPaymentInfoHistory.objects.create(
                
                payment_info_id=int(info_history.id), 
                receipt_number_add=add_history,
                payment_amount_add=add_history,
                student_id=add_history.student_id
                
            )
            
            add_history.delete()
            
        
        paymentInfo.delete()
    
        student.save()
        bed.save()
        
        messages.success(request, "Talaba joydan chiqarildi !")
        return redirect('/dormitory')
       
        
        
    messages.error(request, "Xatolik qaytadan urinib ko'ring !")
    return redirect('/dormitory')


class AddPaymentView(View):
    def post(self, request):
        
        add_payment_info(request)
        
     
        return redirect('/dormitory')
        
        

    
    
class LoginView(View):
    def get(self, request):
        if  request.user.is_authenticated == True:
            return redirect('main:home')
        return render(request, 'auth-login.html')
    
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']


        if  request.user.is_authenticated:
            return redirect('main:home')
            
        user = authenticate(request, username=username, password=password)
        
            
        if user is not None:
            
            if user.is_admin or user.is_staff:
            
                login(request,user)
            
                return redirect('main:home')
        
            if user.is_student:
                
                # login(request,user)
         
                return redirect('student:student-home')
 
        else:
            messages.error(request, "Login yoki parol xato !")
            return redirect('main:login')
                
        
        return render(request, 'auth-login.html')


    
def logOut(request):
    logout(request)
    return redirect('main:login')




# errors views


def handler_404(request, exception):
    return render(request, 'errors/404.html')

def handler_500(request):
    return render(request, 'errors/500.html')