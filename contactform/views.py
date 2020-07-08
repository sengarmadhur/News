from django.shortcuts import render
from django.shortcuts import HttpResponse,render,redirect
# Create your views here.
from .models import ContactForm
import datetime
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
from cat.models import Cat
from myapp.models import article




def contact_add(request):
    now = datetime.datetime.now()
    day = now.day
    year = now.year
    month = now.month
    if len(str(day)) == 1:
        day = '0' + str(day)
    if len(str(month)) == 1:
        month = '0' + str(month)
    date = str(year) + "-" + str(month) + "-" + str(day)
    time = str(now.hour) + ":" + str(now.minute)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        body = request.POST.get('body')

        if name == '' or body == '' or email == '':
            msg = 'All Fields are Required'
            return render(request, 'front/message.html',{'msg':msg})
        b = ContactForm(name=name,email=email,body=body,date=date,time=time)
        b.save()
        msg = 'Thank you for contacting us'
        return render(request, 'front/message.html',{'msg':msg})

    return render(request,'front/message.html')

def contact_show(request):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    msg = ContactForm.objects.all()

    return render(request,'back/contact_form.html',{'msg':msg})

def contact_del(request,id):

    if not request.user.is_authenticated:
        return  redirect('mylogin')

    b = ContactForm.objects.get(pk=id)
    b.delete()
    return  redirect('contact_show')