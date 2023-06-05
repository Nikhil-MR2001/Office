from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all_emp', views.all_emp, name='all_emp'),
    path('add_emp', views.add_emp, name='add_emp'),
    path('remove_emp', views.remove_emp, name='remove_emp'),
    path('remove_emp/<int:id>', views.remove_emp, name='remove_emp'),
    path('filter_emp', views.filter_emp, name='filter_emp'),
    path('update/<int:id>', views.update_emp, name='update_emp'),

    path('msg', views.msg, name='msg'),

    path('login', views.login, name='login'),
    path('register/', views.register, name='register'),
]