from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, request
from django.template import loader
from django import forms
from .dbactions import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import date
import sqlite3
#from .models import
# Create your views here.
mx=0
s=0
@csrf_exempt
def index(request):
    global mx
    global s
    if(mx==0 and s==0):
        return render(request,"homepage.html",{'check':"NOT"},content_type='text/html')
    elif(mx==1):
        mx=0
        return render(request,"homepage.html",{'check':"Exists"},content_type='text/html')
    elif(s==1):
        s=0
        return render(request,"homepage.html",{'check':"NOT Exists"},content_type='text/html')
    elif(s==2):
        s=0
        return render(request,"homepage.html",{'check':"NOT Correct"},content_type='text/html')

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
        "date" : str(date.today()),
        "title" : request.POST['title'],
        "rating" : request.POST['rating'],
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
        user_list = get_user()
        global s
        if(cand_usn not in user_list):
            s=1
            return redirect("/") 
        else:
            s=2
            return redirect("/")

@csrf_exempt
def signup_user(request):
    new_usn = request.POST['usn']
    new_pwd = request.POST['pwd']
    new_email = request.POST['mail']
    new_fname = request.POST['fname']
    new_lname = request.POST['lname']
    picture = request.FILES['pic']
    im = picture.read()
    
    usn_list = get_user()
    if(new_usn in usn_list):
        global mx
        mx=1
        return redirect("/")
    else:
        user = User.objects.create_user(new_usn, email=new_email, password=new_pwd)
        user.first_name = new_fname
        user.last_name = new_lname
        user.save()

        #img upload here
        conn = sqlite3.connect("userpics.db")
        curr = conn.cursor()
        conn.execute("INSERT INTO profilepics VALUES(?,?)", (new_usn,sqlite3.Binary(im)))
        conn.commit()
        conn.close()
        
        if user is not None:
            login(request,user)
            return redirect('/write-review')
        else:
            return redirect('/')

@csrf_exempt
def profile(request):
    uid = User.objects.get(username=request.user.username)
    '''
    column names in db : id,password,username,last_name,first_name,email
    coress name in form: --,pwd,usn,lname,fname,mail
    '''
    
    doc = {'usn':uid.username,'lname':uid.last_name,'fname':uid.first_name,'mail':uid.email}
    return render(request,"profile.html",doc,content_type='text/html')

def logout_user(request):
    logout(request)
    return redirect('/')

def dash_user(request):
    user = request.user.username
    dict_key = {"user":user}
    r1 = get_docs_by_user(dict_key,"Engineering")
    r1+= get_docs_by_user(dict_key,"Arts")
    r1+= get_docs_by_user(dict_key,"Medicine")
    r1+= get_docs_by_user(dict_key,"Law")
    return render(request,"dashboard.html",{'items':r1},content_type='text/html')