from .import views
from django.urls import path,include

from django.conf.urls.static import  static
from django.conf import settings

urlpatterns = [
    path('/panel/newsletter/add/',views.news_letter,name='news_letter'),
    path('/panel/newsletter/emails/',views.news_emails,name='news_emails'),
    path('/panel/newsletter/phones/',views.news_phones,name='news_phones'),
    path('/panel/newsletter/delete/<int:id>/<int:name>',views.news_txt_del,name='news_txt_del'),
]
