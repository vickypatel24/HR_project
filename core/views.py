# Create your views here.
from django.http import HttpResponse
from django.shortcuts import loader
from .models import Course
from .models import Person
from .models import Grade


def core(request):
    return HttpResponse("Hello world!")