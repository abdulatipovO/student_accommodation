# Generated by Django 4.1.6 on 2024-01-03 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_paymentinfo_bedinfohistory'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PaymentInfo',
            new_name='PaymentInfoStudent',
        ),
    ]
