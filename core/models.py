from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.


class Person(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    last_name = models.TextField()
    first_name = models.TextField()
    courses = models.ManyToManyField("Course", blank=True, related_name='person_list')
    active = models.BooleanField(default=True)
    age = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} - {self.age} - {self.gender}'

    class Meta:
        verbose_name_plural = "People"

class Course(models.Model):
    COLOR_CHOICES = (
        ('RED', 'Red'),
        ('YELLOW', 'Yellow'),
        ('GREEN', 'Green'),
        ('ORANGE', 'Orange'),
    )
    name = models.TextField()
    year = models.IntegerField()
    color = models.CharField(max_length=6, choices=COLOR_CHOICES, null=True)

    def __str__(self):
        return f'{self.name} {self.year}'

    class Meta:
        unique_together = ("name", "year", )


class Grade(models.Model):
    objects = object
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.person} {self.grade} {self.course}'


