from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, request
from django.template import loader
from django import forms
from .dbactions import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import sqlite3
#from .models import
# Create your views here.
mx=0
@csrf_exempt
def index(request):
    if(mx==0):
        return render(request,"homepage.html",{'check':"NOT"},content_type='text/html')
    elif(mx==1):
        return render(request,"homepage.html",{'check':"Exists"},content_type='text/html')

@csrf_exempt
def new_review(request):
    c = {'bool':'New'}
    return render(request,"review.html",c,content_type='text/html')

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
        "user":request.user.username,
        "college":request.POST['college'].lower(),
        "course":request.POST['course'].lower(),
        "review":request.POST['review'],
    }
    
    flag = func_upload(db_name,coll_name,doc)

    if flag:
        c = {'bool':'Success'}        
        return render(request,"review.html",c,content_type='text/html')
    else:
        c = {'bool':'Failed'}
        return render(request,"review.html",c,content_type='text/html')

@csrf_exempt
def search(request):
    return render(request,"search.html")

@csrf_exempt
def fetch(request):
    
    college_name = request.POST['college']
    college_name = college_name.replace(" ","")
    college_name = college_name.lower()
    
    kei = { 'course' : request.POST['course'].lower() }
    
    returned = func_retreive(request.POST['branch'],college_name,kei)
    
    res = []
    for x in returned:
        x['college']=x['college'].title()
        x['course']=x['course'].title()
        res.append(x)

    if(len(res)==0):
        c = {'bool':'No'}        
        return render(request,"search.html",c,content_type='text/html')
    else:
        global cx
        cx = {'items':res}
        return redirect('/results')


@csrf_exempt
def results(request):
    return render(request,"results.html",cx,content_type='text/html')

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

    mydb = sqlite3.connect("db.sqlite3")
    mycursor = mydb.cursor()  
    res = mycursor.execute('SELECT username FROM auth_user')
    lis=[]
    for i in res:
        lis.append(i[0])
    if(new_usn in lis):
        global mx
        mx=1
        return redirect("/")
    else:
        user = User.objects.create_user(new_usn, email=new_email, password=new_pwd)
        user.first_name = new_fname
        user.last_name = new_lname
        user.save()
    
        if user is not None:
            login(request,user)
            return redirect('/write-review')
        else:
            return redirect('/')
