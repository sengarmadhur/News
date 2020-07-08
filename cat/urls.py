from .import views

from django.urls import path

urlpatterns = [
    path('panel/categories/list/',views.cat_list,name='cat_list'),
    path('panel/categories/add/',views.cat_add,name='cat_add'),
    path('panel/cat/csv/download/',views.export_cat_csv,name='export_cat_csv'),
     path('panel/cat/csv/import/',views.import_csv,name='import_csv'),
]