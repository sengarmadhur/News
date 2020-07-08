
from django.urls import path,include
from .import views

urlpatterns = [
    path('contact/submit',views.contact_add,name='contact_add'),
    path('panel/contactform',views.contact_show,name='contact_show'),
    path('panel/contactform/del/<int:id>',views.contact_del,name='contact_del'),

]
