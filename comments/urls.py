
from django.contrib import admin
from django.urls import path,include
from .import views
urlpatterns = [
    path('/news/comments/<int:id>',views.add_comments,name='add_comments'),
    path('news/comments/list',views.comments_list,name='comments_list'),
     path('news/comments/delete/<int:id>',views.comments_del,name='comments_del'),
     path('news/comments/confirm/<int:id>',views.comments_confirm,name='comments_confirm'),

]
