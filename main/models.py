from django.db import models
from django.contrib.auth.models import AbstractUser
import re


# Create your models here.

def validate_passport(passport):
    if not re.match(r"[A-Z][A-Z]\d\d\d\d\d\d\d$",passport):
        raise ValueError("Passport raqami noto'g'ri")
    return passport

TYPE_CHOICES  = (
    ("boys", "boys"),
    ("girls", "girls")
)

GENDER_CHOICES  = (
    ("male", "male"),
    ("female", "female")
)


class BaseModel(models.Model):
    created_at = models.DateTimeField("created at", auto_now_add=True)
    updated_at = models.DateTimeField("updated at", auto_now=True)
    
    class Meta:
        abstract = True
        
        
class MonthlyPaymentPrice(BaseModel):
    price = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Oylik to'lov narxi"
        verbose_name_plural = "Oylik to'lov narxlari"  
        


class Accommadation(BaseModel):
    title = models.CharField(verbose_name="Bino nomi", max_length=55)
    type = models.CharField(verbose_name="Bino turi", max_length=10, choices=TYPE_CHOICES, default='boys')
    
    
    def __str__(self):
        return self.title    
    
    class Meta:
        verbose_name = "Bino"
        verbose_name_plural = "Binolar"  
    
    
class Floor(BaseModel):
    accommadation = models.ForeignKey(Accommadation,on_delete=models.CASCADE,related_name="accommadations")
    title = models.CharField(verbose_name="Qavat",max_length=20)
    
    
    def __str__(self):
        return f"{self.title} | {self.accommadation}"
    
    class Meta:
        verbose_name = "Qavat"
        verbose_name_plural = "Qavatlar"  
    
    
class Room(BaseModel):
    floor = models.ForeignKey(Floor,on_delete=models.CASCADE,related_name="floors")
    title = models.CharField(verbose_name="Xona raqami",max_length=20)

    
    def __str__(self):
        return f" {self.title} | {self.floor}"
    
    
    class Meta:
        verbose_name = "Xona"
        verbose_name_plural = "Xonalar"  
    
    
class Bed(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="rooms")
    bed_number = models.CharField(verbose_name="Joy raqami",max_length=20)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.bed_number} | {self.room.title} | {self.room.floor}"
    
    
    class Meta:
        verbose_name = "Joy"
        verbose_name_plural = "Joylar"  
    



class Student(AbstractUser):
    student_id = models.CharField(max_length=12, unique=True)
    first_name = models.CharField(verbose_name="Ismi", max_length=255)
    last_name = models.CharField(verbose_name="Familyasi", max_length=255)
    middle_name = models.CharField(verbose_name="Otasini ismi", max_length=255)
    passport = models.CharField(verbose_name="Passport seriya va raqami",
        max_length=9,unique=True,validators=[validate_passport])
    faculty = models.CharField(verbose_name="Fakultet", max_length=255)
    course_of_study = models.CharField(verbose_name="Ta'lim yo'nalishi", max_length=255)
    stage = models.PositiveIntegerField(verbose_name="Bosqich",default=1)   
    group = models.CharField(verbose_name="Guruh", max_length=20)
    phone = models.CharField(verbose_name="Telefon raqami", max_length=13)
    email = models.EmailField(verbose_name="Elektron pochta manzili")
    gender = models.CharField(verbose_name="JInsi", max_length=10, choices=GENDER_CHOICES, default='male')

    
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True, related_name="beds")
    
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.middle_name} | {self.username}"
    
    
    class Meta:
        verbose_name = "Talaba"
        verbose_name_plural = "Talabalar"  
    
    

    
class PaymentInfo(BaseModel):
    bed = models.ForeignKey(Bed,on_delete=models.CASCADE,related_name="payments")
    student_id = models.CharField(max_length=12)
    
    start_date = models.DateField()
    end_date = models.DateField()
    payment_amount = models.CharField(verbose_name="To'langan summa",max_length=16)
    difference_money = models.CharField(verbose_name="Qoldiq summa",max_length=16)
    
    def __str__(self):
        return f"{self.student_id} & { self.bed }"
    
    class Meta:
        verbose_name = "To'lov info"
        verbose_name_plural = "To'lov infolar"  
    
    
    
class AddPaymentInfo(BaseModel):
    payment_info = models.ForeignKey(PaymentInfo, on_delete=models.CASCADE, related_name="add_payments")
    receipt_number_add = models.CharField(verbose_name="Kvitansiya raqami", max_length=20)
    payment_amount_add = models.CharField(verbose_name="To'langan summa",max_length=16)
    student_id = models.CharField(max_length=12, blank=True, null=True)
    
    class Meta:
        verbose_name = "To'lov kvitansiya"
        verbose_name_plural = "To'lov kvitansiyalari"  
   
   
   
class BedInfoHistory(BaseModel):
    bed = models.ForeignKey(Bed,on_delete=models.PROTECT,related_name="payments_history")
    student_id = models.CharField(max_length=12)
    
    start_date = models.DateField()
    end_date = models.DateField()
    payment_amount = models.CharField(verbose_name="To'langan summa",max_length=16)
    difference_money = models.CharField(verbose_name="Qoldiq summa",max_length=16)
    
    class Meta:
        verbose_name = "To'lov info tarixi"
        verbose_name_plural = "To'lov infolar tarixi"
        
        
        
class AddPaymentInfoHistory(BaseModel):
    payment_info = models.ForeignKey(BedInfoHistory, on_delete=models.CASCADE, related_name="add_payments_history")
    receipt_number_add = models.CharField(verbose_name="Kvitansiya raqami", max_length=20)
    payment_amount_add = models.CharField(verbose_name="To'langan summa",max_length=16)
    student_id = models.CharField(max_length=12, blank=True, null=True)  


    class Meta:
        verbose_name = "To'lov kvitansiya tarixi"
        verbose_name_plural = "To'lov kvitansiyalari tarixi"  


class Application(BaseModel):
    student_id = models.CharField(max_length=12)
    
    
    class Meta:
        verbose_name = "Ariza"
        verbose_name_plural = "Arizalar"



    
