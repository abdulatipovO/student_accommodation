# Generated by Django 4.1.6 on 2024-01-07 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_addpaymentinfo_student_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bedinfohistory',
            name='receipt_number',
        ),
        migrations.RemoveField(
            model_name='paymentinfo',
            name='receipt_number',
        ),
    ]
