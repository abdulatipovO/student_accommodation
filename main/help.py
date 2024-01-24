from .models import *
import datetime
from django.db.models import Sum



def accommadationInfo(accommadations,beds):
    
    accommadation_info = []
    floor_info = []
    room_info = []
    
    for a in accommadations:
        beds_dorm_full = beds.filter(room__floor__accommadation__id=a.id,status=True).count()
        beds_dorm_empty = beds.filter(room__floor__accommadation__id=a.id,status=False).count()
        all_place_dorm = beds_dorm_empty + beds_dorm_full
        
        # ---
        for f in a.accommadations.all():
            
            beds_floor_full = beds.filter(room__floor__id=f.id,status=True).count()
            beds_floor_empty = beds.filter(room__floor__id=f.id,status=False).count()
            all_place_floor = beds_floor_full + beds_floor_empty
        
        
            floor_info.append({
                "floor_id":f.id,
                'beds_floor_full': beds_floor_full,
                'all_place_floor': all_place_floor,
            })
            
            for r in f.floors.all():
                beds_room_full = beds.filter(room__id=r.id,status=True).count()
                beds_room_empty = beds.filter(room__id=r.id,status=False).count()
                all_place_room = beds_room_full + beds_room_empty
            
            
                room_info.append({
                    "room_id":r.id,
                    'beds_room_full': beds_room_full,
                    'all_place_room': all_place_room,
                })
                
            
            
            
            
        accommadation_info.append({
            "accommadation_id":a.id,
            'beds_dorm_full': beds_dorm_full,
            'all_place_dorm': all_place_dorm,
        })
    
    
    
    context = {
        "accommadation_info":accommadation_info,
        "floor_info":floor_info,
        "room_info":room_info,
        
    }
    
    return context




def studentConnectToBed(request):
    student_id = request.POST['student_id']
    receipt_number = request.POST['receipt_number'] #kvitansiya
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    payment_amount = request.POST['payment_amount'] #to'langan summa
    difference_money_hidden = request.POST.get('difference_money_hidden') #qoldiq farq haqiqiy
    
    bed_number_id = request.POST.get('bed_number_id') 
    
    try:
        student = Student.objects.get(id=int(student_id))
        bed = Bed.objects.get(id=int(bed_number_id))
        
    except:
        student = None
        bed = None
    

    if student is not None:
        
        if student.bed == None:
            
            student.bed = bed        
            bed.status = True
            
            student.save()
            bed.save()
      
            PaymentInfo.objects.create(
                bed=bed,
                student_id=student.student_id,
                
                start_date=start_date,
                end_date=end_date,
                payment_amount=payment_amount,
                difference_money=difference_money_hidden
                )
            
            payment_info = PaymentInfo.objects.filter(student_id=student.student_id)[0]
            
            
            add_payment_info = AddPaymentInfo.objects.create(
                
                payment_info_id=int(payment_info.id), 
                receipt_number_add=receipt_number,
                payment_amount_add=payment_amount,
                student_id=payment_info.student_id
                
                )
            
         
            return True
        
    return None



def add_payment_info(request):
    
    id = request.POST['student_id'] 
    receipt_number = request.POST['receipt_number_add']
    payment_amount = request.POST['payment_amount_add']
    
    
    student = Student.objects.filter(is_student=True, id=int(id))[0]
    
    payment = student.bed.payments.all().order_by('id')[0]
    
    add_payment_info = AddPaymentInfo.objects.create(
        payment_info_id=int(payment.id), 
        receipt_number_add=receipt_number,
        payment_amount_add=payment_amount,
        student_id=payment.student_id
        )
    
    main_payment_amout = int(payment.payment_amount)
    main_difference_money = int(payment.difference_money)
    
    main_payment_amout += int(payment_amount)
    main_difference_money -= int(payment_amount)
    
    payment.difference_money = main_difference_money
    payment.payment_amount = main_payment_amout
    
    payment.save()
    
  
    
    return True
    


def CalculationMoney():
    
    today = datetime.datetime.today()
    year = int(today.strftime('%Y'))
    month = int(today.strftime('%m'))

    
    if month < 7:
        autumn_semester_start = datetime.date(year-1, 9, 1)
        autumn_semester_end = datetime.date(year-1, 12, 31)
        
        spring_semester_start = datetime.date(year, 1, 1)
        spring_semester_end = datetime.date(year, 6, 30)
        
    if month > 8:
        autumn_semester_start = datetime.date(year, 9, 1)
        autumn_semester_end = datetime.date(year, 12, 31)
        
        spring_semester_start = datetime.date(year + 1, 1, 1)
        spring_semester_end = datetime.date(year + 1, 6, 30)
        
    
    
    autumn_semester = PaymentInfo.objects.filter(
        start_date__gte=autumn_semester_start, 
        end_date__lte=autumn_semester_end
        ).aggregate(Sum('payment_amount'))
    
    spring_semester = PaymentInfo.objects.filter(
        start_date__gte=spring_semester_start, 
        end_date__lte=spring_semester_end
        ).aggregate(Sum('payment_amount'))
   
    
    return autumn_semester, spring_semester
        
        
