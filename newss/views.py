from django.shortcuts import render
from django.shortcuts import HttpResponse,render,redirect
# Create your views here.
from .models import News
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
from cat.models import Cat
from myapp.models import article
from trending.models import  Trending
import random
from comments.models import Comments 
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from itertools import chain

def about(requests):
    return HttpResponse("<h1>Hello</h1>")


def detail(requests,name):
    news = News.objects.all().order_by("-pk")
    article_var = article.objects.get(pk=2)
    categories = Cat.objects.all()
    sub = SubCat.objects.all()
    lastnews = News.objects.all().order_by("-pk")[:3]
    popularnews = News.objects.all().order_by('-views')
    popularnews2 = News.objects.all().order_by('-views')[:3]
    shownews = News.objects.get(name =name)
    tagsname = News.objects.get(name=name).tags
    tags = tagsname.split(',')
    trending = Trending.objects.all().order_by('-pk')
    code = News.objects.get(name=name).pk
    comments = Comments.objects.filter(news_id=code,status = 1).order_by('-pk')
    comment_count = len(comments)
    try:
        mynews = News.objects.get(name=name)
        mynews.views = mynews.views+1
        mynews.save()
    except:
        print("Can't Increase ")
    return render(requests,'front/detail.html',{'shownews':shownews,'name':article_var,'News':news,'categories':categories,'subcat':sub,'lastnews':lastnews,'popularnews':popularnews,'popularnews2':popularnews2,
    "tags":tags,'trending':trending,'code':code,'comments':comments,'comment_count':comment_count})


def detail_shorturl(requests,id):
    news = News.objects.all().order_by("-pk")
    article_var = article.objects.get(pk=2)
    categories = Cat.objects.all()
    sub = SubCat.objects.all()
    lastnews = News.objects.all().order_by("-pk")[:3]
    popularnews = News.objects.all().order_by('-views')
    popularnews2 = News.objects.all().order_by('-views')[:3]
    shownews = News.objects.get(rand = id)
    tagsname = News.objects.get(rand = id).tags
    tags = tagsname.split(',')
    trending = Trending.objects.all().order_by('-pk')
    comments = Comments.objects.filter(news_id=code,status = 1).order_by('-pk')
    comment_count = len(comments)
    try:
        mynews = News.objects.get(rand = id)
        mynews.views = mynews.views+1
        mynews.save()
    except:
        print("Can't Increase ")
    return render(requests,'front/detail.html',{'shownews':shownews,'name':article_var,'News':news,'categories':categories,'subcat':sub,'lastnews':lastnews,'popularnews':popularnews,'popularnews2':popularnews2,"tags":tags,'trending':trending,'comment_count':comment_count})


def news_list(requests):
    if not requests.user.is_authenticated:
        return redirect('mylogin')
    admin=0
    if requests.user.username == 'admin':
        admin=1
        newss  = News.objects.all()
        paginator = Paginator(newss,1)
        page = requests.GET.get('page')

        try:
            news = paginator.page(page)
        except EmptyPage:
            news = paginator.page(page.num_pages)
        except PageNotAnInteger:
            news = paginator.page(1)


    else:
        news = News.objects.filter(author=requests.user)
    return render(requests,'back/news_list.html',{"news":news,"admin":admin})



def news_add(requests):

    if not requests.user.is_authenticated:
        return redirect('mylogin')

    cat  = SubCat.objects.all()
    now  = datetime.datetime.now()
    day = now.day
    year = now.year
    month = now.month
    if len(str(day)) == 1:
        day = '0' + str(day)
    if len(str(month)) == 1:
        month = '0' + str(month)
    date = str(year) + "-" + str(month) + "-" + str(day)
    randate = str(year)+ str(month) + str(day)
    rand = str(random.randint(1000,9999))
    rand = int(randate + rand)

    while len(News.objects.filter(rand=rand)) !=0 :
        rand = str(random.randint(1000,9999))
        rand = int(randate + rand)

    if(requests.method == "POST"):
        title = requests.POST.get("newstitle")
        category = requests.POST.get("newscat")
        summary = requests.POST.get("newssumm")
        body = requests.POST.get("newsbody")
        newsid = requests.POST.get("newscat")
        catname = SubCat.objects.get(pk=newsid).name
        catid = SubCat.objects.get(pk=newsid).catid
        ocatid = Cat.objects.get(name=SubCat.objects.get(pk=newsid).catname).pk
        tags = requests.POST.get("tags")

        if (title == "" or category == "" or summary == "" or body == ""):
            error = "All Fields are required"
            return render(requests, "back/error.html", {"error": error})
        try:
            fs = FileSystemStorage()
            image = requests.FILES['myfiles']
            filename = fs.save(image.name,image)
            url = fs.url(filename)

            if str(image.content_type).startswith('image'):
                if image.size <= 5000000:
                    d = News(name=title,summary = summary,body=body,date=date,picurl=url,
                             pic=filename,
                             author=requests.user,catname=catname,catid=catid,views=0,
                             ocatid=ocatid,tags = tags,rand=rand)
                    d.save()
                    ud = Cat.objects.get(pk = SubCat.objects.get(pk=newsid).catid)
                    ud.count = ud.count+1
                    ud.save()
                    return redirect('news_list')
                else:
                    fs = FileSystemStorage()
                    fs.delete(filename)
                    error = "Please Upload  image less than 5MB"
                    return render(requests, "back/error.html", {"error": error})
            else:
                fs = FileSystemStorage()
                fs.delete(filename)
                error = "Please Upload The Valid image"
                return render(requests, "back/error.html", {"error": error})

        except:
            fs = FileSystemStorage()
            fs.delete(filename)
            error = "Please Upload The image"
            return render(requests, "back/error.html", {"error": error})



    return render(requests,'back/news_add.html',{'cat':cat})


def news_delete(requests,id):

    if not requests.user.is_authenticated:
        return redirect('mylogin')

    try:
        var = News.objects.get(pk=id)
        ud = Cat.objects.get(pk= var.catid)
        ud.count = ud.count - 1
        ud.save()

        fs = FileSystemStorage()
        fs.delete(str(var.pic))
        var.delete()

    except:
        error = "Something Went Wrong"
        return render(requests, "back/error.html", {"error": error})
    return redirect('news_list')

def news_edit(requests,id):

    if not requests.user.is_authenticated:
        return redirect('mylogin')

    if len(News.objects.filter(pk = id)) == 0:
        error = "News does not exists"
        return render(requests, "back/error.html", {"error": error})

    news = News.objects.get(pk=id)
    cat = SubCat.objects.all()

    if requests.method == "POST":
        title = requests.POST.get("newstitle")
        category = requests.POST.get("newscat")
        summary = requests.POST.get("newssumm")
        body = requests.POST.get("newsbody")
        newsid = requests.POST.get("newscat")
        catname = SubCat.objects.get(pk=newsid).name
        tags = requests.POST.get("tags")

        if (title == "" or category == "" or summary == "" or body == ""):
            error = "All Fields are required"
            return render(requests, "back/error.html", {"error": error})
        try:
            fs = FileSystemStorage()
            image = requests.FILES['myfiles']
            filename = fs.save(image.name, image)
            url = fs.url(filename)

            if str(image.content_type).startswith('image'):
                if image.size <= 5000000:
                    d = News.objects.get(pk=id)

                    fs = FileSystemStorage()
                    fs.delete(str(d.pic))

                    d.name=title
                    d.summary =summary
                    d.body=body
                    d.picurl=url
                    d.pic=filename
                    d.author="Author"
                    d.catname=catname
                    d.catid=newsid
                    d.tags = tags
                    d.act= 0
                    d.save()
                    return redirect('news_list')
                else:
                    fs = FileSystemStorage()
                    fs.delete(filename)
                    error = "Please Upload  image less than 5MB"
                    return render(requests, "back/error.html", {"error": error})
            else:
                fs = FileSystemStorage()
                fs.delete(filename)
                error = "Please Upload The Valid image"
                return render(requests, "back/error.html", {"error": error})

        except:
            d = News.objects.get(pk=id)
            d.name = title
            d.summary = summary
            d.body = body
            d.catname = catname
            d.catid = newsid
            d.tags = tags
            d.save()
            return redirect('news_list')

    return render(requests,'back/news_edit.html',{'id':id,'news':news,'cat':cat})

def news_publish(requests,id):
    
    if not requests.user.is_authenticated:
        return redirect('mylogin')

    news = News.objects.get(pk=id)
    news.act = 1;
    news.save()
    return redirect('news_list')

def show_all_news(request,name):
    catid = Cat.objects.get(name = name).pk
    allnews = News.objects.filter(catid = catid)
    
    news = News.objects.filter(act=1).order_by("-pk")
    article_var = article.objects.get(pk = 2)
    categories = Cat.objects.all()
    sub = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by("-pk")[:3]
    lastnews2 = News.objects.filter(act=1).order_by("-pk")[:4]
    popularnews = News.objects.filter(act=1).order_by('-views')
    popularnews2 = News.objects.filter(act=1).order_by('-views')[:3]

    trending = Trending.objects.all().order_by('-pk')

    return render(request, 'front/all_news.html',{'name':article_var,'News':news,'categories':categories,'subcat':sub,'lastnews':lastnews,
                                                'popularnews':popularnews,
                                                'popularnews2':popularnews2,'trending':trending,'lastnews2':lastnews2,'allnews':allnews})

   
def all_news_all_cats(request):
   
    allnews = News.objects.all()
    
    if request.method == 'POST':
        search = request.POST.get('search')
        catid = request.POST.get('cat')
        f_rom = request.POST.get('from')
        t_o = request.POST.get('to')

        if t_o <f_rom:
            msg = "Your dates are not Compatible"
            return render(request,'front/message.html',{'msg':msg})

        if catid == '0':
            a = News.objects.filter(name__contains = search)
            b = News.objects.filter(summary__contains = search)
            c = News.objects.filter(body__contains = search)
        else:
            a = News.objects.filter(name__contains = search,catid = catid)
            b = News.objects.filter(summary__contains = search,catid = catid)
            c = News.objects.filter(body__contains = search,catid = catid)

    
    
        allnews = list(dict.fromkeys(list(chain(a,b,c))))

    news = News.objects.filter(act=1).order_by("-pk")
    article_var = article.objects.get(pk = 2)
    categories = Cat.objects.all()
    sub = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by("-pk")[:3]
    lastnews2 = News.objects.filter(act=1).order_by("-pk")[:4]
    popularnews = News.objects.filter(act=1).order_by('-views')
    popularnews2 = News.objects.filter(act=1).order_by('-views')[:3]

    trending = Trending.objects.all().order_by('-pk')

    now  = datetime.datetime.now()
    day = now.day
    year = now.year
    month = now.month
    if len(str(day)) == 1:
        day = '0' + str(day)
    if len(str(month)) == 1:
        month = '0' + str(month)
    date = str(year) + "-" + str(month) + "-" + str(day)
    f_rom = []
    t_o = []
    for i in range(30):
        b = datetime.datetime.now() - datetime.timedelta(days=i)
        day = b.day
        year = b.year
        month = b.month
        if len(str(day)) == 1:
            day = '0' + str(day)
        if len(str(month)) == 1:
            month = '0' + str(month)
        b = str(year) + "-" + str(month) + "-" + str(day)
        f_rom.append(b)
    for i in range(30):
        c = datetime.datetime.now() + datetime.timedelta(days=i)
        day = c.day
        year = c.year
        month = c.month
        if len(str(day)) == 1:
            day = '0' + str(day)
        if len(str(month)) == 1:
            month = '0' + str(month)
        c = str(year) + "-" + str(month) + "-" + str(day)
        t_o.append(c)

    return render(request, 'front/all_news_all_cats.html',{'name':article_var,'News':news,'categories':categories,'subcat':sub,'lastnews':lastnews,
                                                'popularnews':popularnews,
                                                'popularnews2':popularnews2,'trending':trending,'lastnews2':lastnews2,'allnews':allnews,'f_rom':f_rom,'t_o':t_o})


def all_news_all_cat_search(request):
    
    if request.method == 'POST':
        search = request.POST.get('search')
        catid = request.POST.get('cat')
        f_rom = request.POST.get('from')
        t_o = request.POST.get('to')


        if t_o < f_rom and t_o != '0' and f_rom != '0':
            msg = "Your dates are not Compatible"
            return render(request,'front/message.html',{'msg':msg})


        if catid == '0':
            if f_rom != '0' and t_o != '0':
                a = News.objects.filter(name__contains = search,date__gte=f_rom,date__lte=t_o)
                b = News.objects.filter(summary__contains = search,date__gte=f_rom,date__lte=t_o)
                c = News.objects.filter(body__contains = search,date__gte=f_rom,date__lte=t_o)
            elif t_o != '0':
                a = News.objects.filter(name__contains = search,date__lte=t_o)
                b = News.objects.filter(summary__contains = search,date__lte=t_o)
                c = News.objects.filter(body__contains = search,date__lte=t_o)
            elif f_rom != '0':
                a = News.objects.filter(name__contains = search,date__gte=f_rom)
                b = News.objects.filter(summary__contains = search,date__gte=f_rom)
                c = News.objects.filter(body__contains = search,date__gte=f_rom)
            else:
                a = News.objects.filter(name__contains = search)
                b = News.objects.filter(summary__contains = search)
                c = News.objects.filter(body__contains = search)
            
                
           
                
               
        else:
            if f_rom != '0' and t_o != '0':
                a = News.objects.filter(name__contains = search,catid=catid,date__gte=f_rom,date__lte=t_o)
                b = News.objects.filter(summary__contains = search,catid=catid,date__gte=f_rom,date__lte=t_o)
                c = News.objects.filter(body__contains = search,catid=catid,date__gte=f_rom,date__lte=t_o)
            elif t_o != '0':
                a = News.objects.filter(name__contains = search,catid=catid,date__lte=t_o)
                b = News.objects.filter(summary__contains = search,catid=catid,date__lte=t_o)
                c = News.objects.filter(body__contains = search,catid=catid,date__lte=t_o)
            elif f_rom != '0':
                a = News.objects.filter(name__contains = search,catid=catid,date__gte=f_rom)
                b = News.objects.filter(summary__contains = search,catid=catid,date__gte=f_rom)
                c = News.objects.filter(body__contains = search,catid=catid,date__gte=f_rom)
            else:
                a = News.objects.filter(name__contains = search,catid=catid)
                b = News.objects.filter(summary__contains = search,catid=catid)
                c = News.objects.filter(body__contains = search,catid=catid)
            

    
    
        allnews = list(dict.fromkeys(list(chain(a,b,c))))
    
    news = News.objects.filter(act=1).order_by("-pk")
    article_var = article.objects.get(pk = 2)
    categories = Cat.objects.all()
    sub = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by("-pk")[:3]
    lastnews2 = News.objects.filter(act=1).order_by("-pk")[:4]
    popularnews = News.objects.filter(act=1).order_by('-views')
    popularnews2 = News.objects.filter(act=1).order_by('-views')[:3]

    trending = Trending.objects.all().order_by('-pk')


    now  = datetime.datetime.now()
    day = now.day
    year = now.year
    month = now.month
    if len(str(day)) == 1:
        day = '0' + str(day)
    if len(str(month)) == 1:
        month = '0' + str(month)
    date = str(year) + "-" + str(month) + "-" + str(day)
    f_rom = []
    t_o = []
    for i in range(30):
        b = datetime.datetime.now() - datetime.timedelta(days=i)
        day = b.day
        year = b.year
        month = b.month
        if len(str(day)) == 1:
            day = '0' + str(day)
        if len(str(month)) == 1:
            month = '0' + str(month)
        b = str(year) + "-" + str(month) + "-" + str(day)
        f_rom.append(b)
    for i in range(30):
        c = datetime.datetime.now() + datetime.timedelta(days=i)
        day = c.day
        year = c.year
        month = c.month
        if len(str(day)) == 1:
            day = '0' + str(day)
        if len(str(month)) == 1:
            month = '0' + str(month)
        c = str(year) + "-" + str(month) + "-" + str(day)
        t_o.append(c)


    return render(request, 'front/all_news_all_cats.html',{'name':article_var,'News':news,'categories':categories,'subcat':sub,'lastnews':lastnews,
                                                'popularnews':popularnews,
                                                'popularnews2':popularnews2,'trending':trending,'lastnews2':lastnews2,'allnews':allnews,'f_rom':f_rom,'t_o':t_o})


















