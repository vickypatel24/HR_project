# Generated by Django 4.2 on 2023-06-21 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0012_userotp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userotp',
            name='otp',
            field=models.IntegerField(),
        ),
    ]