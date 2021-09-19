from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, request
from django.template import loader
from django import forms
from .dbactions import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
#from .models import
# Create your views here.

@csrf_exempt
def index(request):
    return render(request,"homepage.html")

@csrf_exempt
def new_review(request):
    return render(request,"review.html")

@csrf_exempt
def upload_review(request):
    
    db_name = request.POST['branch']
    
    college_name = request.POST['college']
    college_name = college_name.replace(" ","")
    college_name = college_name.lower()
    
    course_name = request.POST['course']
    course_name = course_name.replace(" ","")
    course_name = course_name.lower()
    
    coll_name = college_name
    
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

@csrf_exempt
def upload_success(request):
    return HttpResponse("Your review was recorded Successfully")

@csrf_exempt
def upload_failed(request):
    return HttpResponse("Something is not right, Please Try Again")

@csrf_exempt
def search(request):
    return render(request,"search.html")

@csrf_exempt
def fetch(request):
    
    college_name = request.POST['college']
    college_name = college_name.replace(" ","")
    college_name = college_name.lower()
    
    kei = { 'course' : request.POST['course'] }
    
    returned = func_retreive(request.POST['branch'],college_name,kei)
    
    res = []
    for x in returned:
        res.append(x)

    if(len(res)==0):
        return redirect('/noresults')

    global c
    c = {'items':res}
    
    return redirect('/results')

@csrf_exempt
def results(request):
    return render(request,"results.html",c,content_type='text/html')

@csrf_exempt
def noresults(request):
    return HttpResponse("No Reviews Found :(")

@csrf_exempt
def login_user(request):
    
    cand_usn = request.POST['UN']
    cand_pwd = request.POST['PW']
    user = authenticate(request, username = cand_usn, password = cand_pwd)
    if user is not None:
        login(request, user)
        return redirect('/write-review')
    else:
        return redirect('/')

@csrf_exempt
def signup_user(request):
    
    new_usn = request.POST['usn']
    new_pwd = request.POST['pwd']
    new_email = request.POST['mail']
    new_fname = request.POST['fname']
    new_lname = request.POST['lname']
    
    user = User.objects.create_user(new_usn, email=new_email, password=new_pwd)
    
    user.first_name = new_fname
    user.last_name = new_lname
    user.save()
    
    if user is not None:
        login(request,user)
        return redirect('/write-review')
    else:
        return redirect('/')
