from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, request
from django.template import loader
from django import forms
from .dbactions import *
#from .models import
# Create your views here.

@csrf_exempt
def index(request):
    return HttpResponse("This is the Default Page of Cafe Review, Users are not supposed to see this")

@csrf_exempt
def new_review(request):
    return render(request,"review.html")

@csrf_exempt
def upload_review(request):
    db_name = request.POST['branch']
    college_name = request.POST['college']
    college_name = college_name.replace(" ","")
    college_name = college_name.lower()
    print(college_name)
    coll_name = college_name
    doc = {
        "college":college_name,
        "course":request.POST['course'],
        "review":request.POST['review'],
    }
    flag = func_upload(db_name,coll_name,doc)
    if flag:
        return redirect('/upload-success')
    else:
        return redirect('/upload-failed')

@csrf_exempt
def upload_success(request):
    return HttpResponse("Your review was recorded Successfully")

@csrf_exempt
def upload_failed(request):
    return HttpResponse("Something is not right, Please Try Again")
