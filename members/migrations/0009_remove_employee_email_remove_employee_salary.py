# Generated by Django 4.2 on 2023-04-13 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_employee_email_employee_salary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='email',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='salary',
        ),
    ]
