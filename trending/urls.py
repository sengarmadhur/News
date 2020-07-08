from .import views

from django.urls import path

urlpatterns = [
    path('panel/trending/',views.trending_add,name='trending_add'),
    path('panel/trending/delete/<int:id>',views.trending_del,name='trending_del'),
    path('panel/trending/edit/<int:id>',views.trending_edit,name='trending_edit'),
    
]