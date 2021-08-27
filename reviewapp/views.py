from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, request
from django.template import loader
from django import forms
from .dbactions import *
#from .models import
# Create your views here.

def index(request):
    return HttpResponse("This is the Default Page of Cafe Review, Users are not supposed to see this")

@csrf_exempt
def new_review(request):
    return render(request,"review.html")

@csrf_exempt
def upload_review(request):
    db_name = request.POST['branch']
    coll_name = request.POST['college']
    doc = {
        "college":request.POST['college'],
        "course":request.POST['course'],
        "review":request.POST['review'],
    }
    flag = func_upload(db_name,coll_name,doc)
    if flag:
        return redirect('/upload-success')
    else:
        return redirect('/upload-failed')

def upload_success(request):
    return HttpResponse("Your review was recorded Successfully")

def upload_failed(request):
    return HttpResponse("Something is not right, Please Try Again")
