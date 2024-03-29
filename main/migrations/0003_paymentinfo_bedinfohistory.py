# Generated by Django 4.1.6 on 2024-01-03 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_student_is_admin_student_is_student_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('student_id', models.CharField(max_length=12, unique=True)),
                ('receipt_number', models.CharField(max_length=20, verbose_name='Kvitansiya raqami')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('payment_amount', models.CharField(max_length=16, verbose_name="To'langan summa")),
                ('difference_money', models.CharField(max_length=16, verbose_name='Qoldiq summa')),
                ('bed', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='main.bed')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BedInfoHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('student_id', models.CharField(max_length=12, unique=True)),
                ('receipt_number', models.CharField(max_length=20, verbose_name='Kvitansiya raqami')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('payment_amount', models.CharField(max_length=16, verbose_name="To'langan summa")),
                ('difference_money', models.CharField(max_length=16, verbose_name='Qoldiq summa')),
                ('bed', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments_history', to='main.bed')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
