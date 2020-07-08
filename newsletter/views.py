from django.shortcuts import render,redirect
import newss
from django.shortcuts import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import Newsletter
from newss.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import login,logout,authenticate
from trending.models import Trending
from django.contrib.auth.models import User
from manager.models import Manager

def news_letter(request):
    if request.method == 'POST':
        txt = request.POST.get('txt')
        result = txt.find('@')

        if int(result) != -1:
            b = Newsletter(txt=txt,status=1)
            b.save()
        else:
            try:
                txt = int(txt)
                b = Newsletter(txt=txt,status=2)
                b.save()
            except:
                return redirect('index')
    return redirect('index')


def news_emails(request):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    emails = Newsletter.objects.filter(status=1)

    return render(request,'back/emails.html',{'emails':emails})

def news_phones(request):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    phones = Newsletter.objects.filter(status=2)

    return render(request,'back/phones.html',{'phones':phones})

def news_txt_del(request,id,name):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    b = Newsletter.objects.get(pk=id)
    b.delete()

    emails = Newsletter.objects.filter(status=1)
    phones = Newsletter.objects.filter(status=2)

    if int(name) == 1:
        return redirect('news_emails')

    return redirect('news_phones')