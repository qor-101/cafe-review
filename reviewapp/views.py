from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
#from .models import
# Create your views here.

def index(request):
    return HttpResponse("This is the Default Page of Cafe Review, Users are not supposed to see this")
