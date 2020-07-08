from django.shortcuts import render,redirect
from .models import SubCat
# Create your views here.
from cat.models import Cat



def subcat_list(request):
    if not request.user.is_authenticated:
        return redirect('mylogin')

    subcat = SubCat.objects.all();
    return render(request,'back/subcat_list.html',{'subcat':subcat})

def subcat_add(request):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    cat  = Cat.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        catid = request.POST.get('cat')
        catname = Cat.objects.get(pk=catid).name
        if name == "":
            error = "Please Enter A Category"
            return render(request, "back/error.html", {"error": error})
        if len(SubCat.objects.filter(name=name)):
            error = "This Sub Category Already Exists"
            return render(request, "back/error.html", {"error": error})
        b = SubCat(name = name,catname = catname,catid = catid)
        b.save()
        return  redirect('subcat_list')


    return render(request,'back/subcat_add.html',{'cat':cat})