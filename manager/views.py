from django.shortcuts import render,redirect
import newss
from django.shortcuts import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import Manager
from newss.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import login,logout,authenticate
from trending.models import Trending
from django.contrib.auth.models import User,Group,Permission
from django.contrib.contenttypes.models import ContentType

def manager_list(request):
    
    manager = Manager.objects.all()

    return render(request,'back/manager_list.html',{'manager':manager})


def manager_del(request,id):
    
    manager = Manager.objects.get(pk=id)
    b = User.objects.filter(username=manager.uname)
    b.delete()
    manager.delete()

    return redirect('manager_list')

def manager_group(request):
    
    prem = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser':
            prem = 1
    
    if prem == 0:
        error = "Acces Denied"
        return render(request,'back/error.html',{'error':error})

    group =Group.objects.all().exclude(name= 'masteruser')

    return render(request,'back/manager_group.html',{'group':group})

def manager_group_add(request):

    prem = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser':
            prem = 1
    
    if prem == 0:
        error = "Acces Denied"
        return render(request,'back/error.html',{'error':error})

    if request.method  == 'POST':
        gname = request.POST.get('groupname')
        if len(Group.objects.filter(name=gname)) == 0:
            g = Group(name = gname)
            g.save()
    return redirect('manager_group')

def manager_group_del(request,name):
    
    prem = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser':
            prem = 1
    
    if prem == 0:
        error = "Acces Denied"
        return render(request,'back/error.html',{'error':error})

    g = Group.objects.filter(name=name)
    g.delete()

    return redirect('manager_group')

def user_group(request,id):
    
    manager = Manager.objects.get(pk=id)
    user = User.objects.get(username = manager.uname)
    user_group = []
    for i in user.groups.all():
        user_group.append(i.name)
    
    group = Group.objects.all()

    return render(request,'back/user_group.html',{'user_group':user_group,'group':group,'id':id})

def add_user_to_group(request,id):

    if request.method == 'POST':
        gname = request.POST.get('ugroup')
        group = Group.objects.get(name=gname)
        manager = Manager.objects.get(pk=id)
        user = User.objects.get(username= manager.uname)
        user.groups.add(group)
    return redirect('user_group',id)

def del_user_to_group(request,id,name):
    group = Group.objects.get(name = name)
    user =  Manager.objects.get(pk=id)
    user = User.objects.get(username = user.uname)
    user.groups.remove(group)
    return redirect('user_group',id)

def manager_perms(request):
    
    prem = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser':
            prem = 1
    
    if prem == 0:
        error = "Acces Denied"
        return render(request,'back/error.html',{'error':error})

    perms = Permission.objects.all()

    return render(request,'back/manager_perms.html',{'perms':perms})

def manager_perms_del(request,name):
    
    prem = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser':
            prem = 1
    
    if prem == 0:
        error = "Acces Denied"
        return render(request,'back/error.html',{'error':error})

    perms = Permission.objects.filter(name = name)
    perms.delete()

    return redirect('manager_perms')

def manager_perms_add(request):
    
    prem = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser':
            prem = 1
    
    if prem == 0:
        error = "Acces Denied"
        return render(request,'back/error.html',{'error':error})

    if request.method == 'POST':
        permname = request.POST.get('permname')
        codename = request.POST.get('codename')
        try:
            content_type = ContentType.objects.get(app_label='myapp',model ='article')
            Permission.objects.create(codename=codename,name=permname,content_type=content_type)
        except:
            msg = "Permission already exists"
            return render(request,'front/message.html',{'msg':msg})
    return redirect('manager_perms')

def user_perms(request,id):
    
    manager = Manager.objects.get(pk=id)
    user = User.objects.get(username = manager.uname)
    user_perms = []
    permission = Permission.objects.filter(user=user)
   
    for i in permission:
        user_perms.append(i.name)
    
    perms  = Permission.objects.all()

    return render(request,'back/user_perms.html',{'user_perms':user_perms,'id':id,'perms':perms})

def user_perms_del(request,id,name):
    
    manager = Manager.objects.get(pk=id)
    user = User.objects.get(username = manager.uname)
    permission = Permission.objects.get(name=name)
    user.user_permissions.remove(permission)
    
    return redirect('user_perms',id) 

def user_perms_add(request,id):
    
    if request.method == 'POST':
        pname = request.POST.get('pname') 
        manager = Manager.objects.get(pk=id)
        user = User.objects.get(username = manager.uname)
        permission = Permission.objects.get(name=pname)
        user.user_permissions.add(permission)
    
    return redirect('user_perms',id)    

def group_perms(request,name):
    group = Group.objects.get(name=name)
    perms = group.permissions.all()
    allperms = Permission.objects.all()
    return render(request,'back/group_perms.html',{'perms':perms,'name':name,'allperms':allperms})

def group_perms_del(request,gname,name):
   
   group = Group.objects.get(name=gname)
   perm = Permission.objects.get(name=name)

   group.permissions.remove(perm)

   return redirect('group_perms',name=gname)

def group_perms_add(request,name):

    if request.method == 'POST':
        group = Group.objects.get(name=name)
        pname = request.POST.get('pname')
        perm = Permission.objects.get(name=pname)
        group.permissions.add(perm) 
   

    return redirect('group_perms',name=name)