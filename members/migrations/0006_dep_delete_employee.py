# Generated by Django 4.2 on 2023-04-11 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_employee_delete_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dep_name', models.CharField(max_length=255)),
                ('dep_location', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
    ]