from django.shortcuts import render
from django.shortcuts import HttpResponse,render,redirect
# Create your views here.
from .models import Comments
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
from cat.models import Cat
from myapp.models import article
from newss.models import News
from manager.models import Manager
from trending.models import  Trending
import random
import datetime

def add_comments(request,id):
    
    
    
    if request.method == 'POST':
        
        now  = datetime.datetime.now()
        day = now.day
        year = now.year
        month = now.month
        if len(str(day)) == 1:
            day = '0' + str(day)
        if len(str(month)) == 1:
            month = '0' + str(month)
        date = str(year) + "-" + str(month) + "-" + str(day)
        time= str(now.hour) + ":" + str(now.minute)
        comment = request.POST.get('msg')
        if request.user.is_authenticated:
            manager = Manager.objects.get(uname=request.user)

            b = Comments(name=manager.name,email=manager.email,comments=comment,news_id=id,date=date,time=time)
            b.save()
        else:
            name = request.POST.get('name')
            email = request.POST.get('email')
            b = Comments(name=name,email=email,comments=comment,news_id=id,date=date,time=time)
            b.save()
    
    name = News.objects.get(pk=id).name
    return redirect('detail',name=name)

def comments_list(request):
    
    if not request.user.is_authenticated:
        return redirect('mylogin')
    comments = Comments.objects.all()
    return render(request,'back/comments_list.html',{'comments':comments})

def comments_del(request,id):
    
    if not request.user.is_authenticated:
        return redirect('mylogin')
    
    comment = Comments.objects.get(pk=id)
    comment.delete()
    return redirect('comments_list')

def comments_confirm(request,id):
    
    if not request.user.is_authenticated:
        return redirect('mylogin')
    
    comment = Comments.objects.get(pk=id)
    comment.status = 1
    comment.save()
    return redirect('comments_list')





























































































