from .import views
from django.urls import path,include

from django.conf.urls.static import  static
from django.conf import settings
from rest_framework import routers


router = routers.DefaultRouter()
router.register('mynews',views.NewsViewSet)

urlpatterns = [
    path('rest/',include(router.urls)),
    path('api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('',views.index,name='index'),
    path('about/', views.about, name='about'),
    path('panel/',views.admin_panel,name='panel'),
    path('login/',views.mylogin,name='mylogin'),
    path('register/',views.myregister,name='myregister'),
    path('logout/', views.mylogout, name='mylogout'),
    path('panel/setting/',views.site_setting,name='site_setting'),
    path('panel/about/setting/',views.about_setting,name='about_setting'),
    path('contact/',views.contact,name='contact'),
    path('panel/change/password/',views.change_password,name='change_password'),
    path('data/json/',views.data_json,name='data_json'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)