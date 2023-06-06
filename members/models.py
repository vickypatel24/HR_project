from django.db import models

# gender_choices = [
#   ('male', 'Male'),
#   ('female', 'Female')
# ]

# Create your models here.
# class Member(models.Model):
#   firstname = models.CharField(max_length=255)
#   lastname = models.CharField(max_length=255)
#   phone = models.IntegerField()
#   joined_date = models.DateField(auto_now_add=True)
#   gender = models.CharField(max_length=50, choices=gender_choices)


class Dep(models.Model):
  dep_name = models.CharField(max_length=255)
  dep_location = models.CharField(max_length=255)

  def __str__(self):
    return self.dep_name


class Employee(models.Model):
  f_name = models.CharField(max_length=255)
  l_name = models.CharField(max_length=255)
  age = models.IntegerField()
  dep = models.ForeignKey('Dep', on_delete=models.CASCADE)
  salary = models.IntegerField(null=True)
  email = models.EmailField(max_length=254, null=True)
  active = models.BooleanField(default=True)

  # def __str__(self):
  #   return f'{self.f_name} {self.l_name}'


class UserOtp(models.Model):
  user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
  otp = models.IntegerField()
