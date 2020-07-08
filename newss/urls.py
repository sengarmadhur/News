
from django.contrib import admin
from django.urls import path,include
from .import views
urlpatterns = [
    path('newss/',views.about),
    path('newss/<str:name>',views.detail,name='detail'),
     path('url/<int:id>',views.detail_shorturl,name='detail_shorturl'),
    path('panel/news/list',views.news_list,name='news_list'),
    path('panel/news/add',views.news_add,name='news_add'),
path('panel/news/delete/<int:id>',views.news_delete,name='news_delete'),
path('panel/news/edit/<int:id>',views.news_edit,name='news_edit'),
path('panel/news/publish/<int:id>',views.news_publish,name='news_publish'),
path('/show/all/news/<str:name>',views.show_all_news,name='show_all_news'),
path('/show/all/news/all/categories/',views.all_news_all_cats,name='all_news_all_cats'),
path('/show/news/search/',views.all_news_all_cat_search,name='all_news_all_cat_search'),


]
