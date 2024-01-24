from django.views import View
from main.models import Student, Application
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib import messages


class SearchStudent(View):
    def get(self, request):
        value = request.GET.get('value')
        
        result = {
            "status":200,
            "data":[]
        }
        
        value = value.strip() if value else None
        
        if value:
            student = Student.objects.filter(id=int(value))
            
            for s in student:
                result['data'].append(
                    {
                        "student_id":s.student_id,                        
                        'first_name':s.first_name,
                        'last_name':s.last_name,
                        "middle_name":s.middle_name,
                        "faculty":s.faculty,
                        "course_of_study":s.course_of_study,
                        "stage":s.stage,
                        "group":s.group
                        
                        
                    }
                )
            
        return JsonResponse(result)
    
class GetPaymentInfo(View):
    def get(self, request):
        
        value = request.GET.get('value')
        
        result = {
            "status":200,
            "data":[],
            "total_info":[]
        }
        
        value = value.strip() if value else None
        
        if value:
            student = Student.objects.filter(is_student=True, id=int(value))[0]
            payments = student.bed.payments.all()[0]
            add_payment_info = payments.add_payments.all()
            
            
            
            for p in add_payment_info:
                    result['data'].append(
                        {
                            "student_id":p.student_id,                        
                            "payment_amount":p.payment_amount_add,                        
                            "receipt_number":p.receipt_number_add,                        
                                                
                            
                        }
            )
            result['total_info'].append({
                "difference_money":payments.difference_money,
                "payment_amount":payments.payment_amount,
            })
        
        
        
        return JsonResponse(result)


class ApplicationLoginView(View):
    def post(self, request):
        
        username = request.POST['username'].strip('')
        password = request.POST['password'].strip('')

        result = {
            "status":200,
            "data":[],
            "message":[]
        }
        
        user = authenticate(request, username=username, password=password)
        
            
     
        if user is not None:
            
            Application.objects.create(student_id=user.student_id)
            
            messages.success(request, "Arizangiz yuborildi!")
        
        else:
            msg = "Login yoki parol xato !"
            result['status'] = 401
            result['message'].append(msg)
        

        return JsonResponse(result)
    