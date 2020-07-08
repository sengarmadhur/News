from django.shortcuts import render
from django.shortcuts import HttpResponse,render,redirect
# Create your views here.
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
from cat.models import Cat
from .models import Trending

def trending_add(request):

    if not request.user.is_authenticated:
        return redirect('mylogin')
        
    trending = Trending.objects.all()
    if request.method == 'POST':
        trend = request.POST.get('trending')
        if trend == '':
            error = "All Fiels are required"
            return render(request,'back/error.html',{'error':error})
        b = Trending(headline=trend)
        b.save()
    return render(request,'back/trending.html',{'trending':trending})


def trending_del(request,id):
    
    if not request.user.is_authenticated:
        return redirect('mylogin')
    
    b = Trending.objects.get(pk=id)
    b.delete()
    trending = Trending.objects.all()
    return render(request,'back/trending.html',{'trending':trending})

def trending_edit(request,id):
    
    
        
    if not request.user.is_authenticated:
        return redirect('mylogin')
    
    if request.method == 'POST':
        b = Trending.objects.get(pk=id)
        headline = request.POST.get('headline')
        if headline == '':
            error = "All Fields are required"
            return render(request,"back/error.html",{'error':error})
        b.headline = headline
        b.save()
        return redirect('trending_add')
    
    headline = Trending.objects.get(pk=id).headline

    return render(request,'back/trending_edit.html',{'headline':headline,'id':id})