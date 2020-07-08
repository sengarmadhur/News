from django.shortcuts import render,redirect
import newss
from django.shortcuts import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import article
from newss.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import login,logout,authenticate
from trending.models import Trending
from django.contrib.auth.models import User
from manager.models import Manager
import random
import string
from bs4 import BeautifulSoup
from urllib import request as req
from .serializer import NewsSerializer
from rest_framework import viewsets
from django.http import JsonResponse
from newsletter.models import Newsletter


def index(requests):
    news = News.objects.filter(act=1).order_by("-pk")
    article_var = article.objects.get(pk = 2)
    categories = Cat.objects.all()
    sub = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by("-pk")[:3]
    lastnews2 = News.objects.filter(act=1).order_by("-pk")[:4]
    popularnews = News.objects.filter(act=1).order_by('-views')
    popularnews2 = News.objects.filter(act=1).order_by('-views')[:3]

    trending = Trending.objects.all().order_by('-pk')

    return render(requests, 'front/index.html',{'name':article_var,'News':news,'categories':categories,'subcat':sub,'lastnews':lastnews,
                                                'popularnews':popularnews,
                                                'popularnews2':popularnews2,'trending':trending,'lastnews2':lastnews2})

def about(request):
    news = News.objects.all().order_by("-pk")
    article_var = article.objects.get(pk=2)
    categories = Cat.objects.all()
    sub = SubCat.objects.all()
    lastnews = News.objects.all().order_by("-pk")[:3]
    popularnews = News.objects.all().order_by('-views')
    popularnews2 = News.objects.all().order_by('-views')[:3]

    trending = Trending.objects.all().order_by('-pk')

    return render(request, 'front/about.html',
                  {'name': article_var, 'News': news, 'categories': categories, 'subcat': sub, 'lastnews': lastnews,
                   'popularnews': popularnews, 'popularnews2': popularnews2,'trending':trending})


def about_setting(request):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    if request.method == 'POST':
        body = request.POST.get('aboutbody')
        if body == '':
            error = "All Fields Are required"
            return render(request, "back/error.html", {"error": error})
        d = article.objects.get(pk=2)
        d.bodylong = body
        d.save()


    aboutbody = article.objects.get(pk=2).bodylong

    return render(request,'back/about_setting.html',{'aboutbody':aboutbody})


def admin_panel(request):

    if not request.user.is_authenticated:
        return redirect('mylogin')
    
    randstr = "" 
    spchar = ['@','$','#','^','%','!','*']
    for i in range(10):
        randstr = randstr + random.choice(string.ascii_letters)
        randstr+=random.choice(spchar)
        randstr+=str(random.randint(0,9))
    
    count = News.objects.count()
    randnews = News.objects.all()[random.randint(0,count-1)]
    randnum = random.randint(1000000,999999999999999999)
    return render(request,'back/home.html',{'randstr':randstr,'randnews':randnews,'randnum':randnum})

def mylogin(request):

    if request.method == 'POST':
        user = request.POST.get('username')
        upass = request.POST.get('password')

        if user!="" and upass!="":
            user = authenticate(username=user,password=upass)
            if user != None:
                login(request,user)
                return  redirect('panel')
    return render(request,'front/login.html')

def myregister(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        if password != password1:
            msg = "Password is not matching"
            return render(request,'front/message.html',{'msg':msg})
        
        if len(User.objects.filter(username=uname))!=0 and len(User.objects.filter(email =email))!=0:
            msg = "User already exists"
            return render(request,'front/message.html',{'msg':msg})
        user =  User.objects.create_user(username=uname,email=email,password=password)
        user.save()
        b = Manager(name=name,uname=uname,email=email)
        b.save()

        return redirect('mylogin')
    
    return render(request,'front/login.html')


def mylogout(request):
    logout(request)
    return  redirect('mylogin')

def site_setting(request):

    if not request.user.is_authenticated:
        return render('mylogin')
    if request.method == "POST":
        title = request.POST.get('title')
        body = request.POST.get('body')
        fb = request.POST.get('fb')
        tw = request.POST.get('tw')
        insta = request.POST.get('insta')
        ph = request.POST.get('ph')

        b = article.objects.get(pk =2)

        if fb == "":fb="#"
        if tw == "":tw="#"
        if insta == "":insta="#"

        if title == "" or ph == "" or body == "":
            error = "All Fields Are required"
            return render(request,"back/error.html",{"error":error})
        try:
            fs = FileSystemStorage()
            image = request.FILES['myfiles']
            filename = fs.save(image.name,image)
            url = fs.url(filename)
            b.picname = filename
            b.picurl = url
            b.fb = fb
            b.tw = tw
            b.title = title
            b.body = body
            b.insta = insta
            b.ph = ph
            b.save()
        except:
            b.fb = fb
            b.tw = tw
            b.title =title
            b.body = body
            b.insta = insta
            b.ph = ph
            b.save()
        try:
            fs = FileSystemStorage()
            image2 = request.FILES['myfiles2']
            filename = fs.save(image2.name, image2)
            url = fs.url(filename)
            b.picname2 = filename
            b.picurl2 = url
            b.save()
        except:
            b.picurl2 = ""
            b.picname2 = ""
            b.save()



    site = article.objects.get(pk = 2)
    return render(request,'back/setting.html',{'site':site})

def contact(request):
    news = News.objects.all().order_by("-pk")
    article_var = article.objects.get(pk=2)
    categories = Cat.objects.all()
    sub = SubCat.objects.all()
    lastnews = News.objects.all().order_by("-pk")[:3]
    popularnews = News.objects.all().order_by('-views')
    popularnews2 = News.objects.all().order_by('-views')[:3]

    trending = Trending.objects.all().order_by('-pk')

    return render(request, 'front/contact.html',
                  {'name': article_var, 'News': news, 'categories': categories, 'subcat': sub, 'lastnews': lastnews,
                   'popularnews': popularnews, 'popularnews2': popularnews2,'trending':trending})


def change_password(request):
    
    if not request.user.is_authenticated:
        return redirect('mylogin')
    
    if request.method == 'POST':
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')

        if oldpassword == "" or newpassword == "":
            error = "All fields are required"
            return render(request,"back/error.html",{"error":error})
        
        user = authenticate(username = request.user,password=oldpassword)

        if user != None:
           
            if len(newpassword)<4:
               error = "Password must contains atleast 4 characters"
               return render(request,"back/error.html",{"error":error})
            user = User.objects.get(username=request.user)
            user.set_password(newpassword)
            user.save()
            return redirect('mylogout')
            

        else:
            error = "Old Password is Incorrect"
            return render(request,"back/error.html",{'error':error})
    
    return render(request,'back/changepass.html')


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

def data_json(request):
    
    count = Newsletter.objects.filter(status = 1).count()
    data = {'Count':count}

    return JsonResponse(data)