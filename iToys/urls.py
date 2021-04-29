from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('main', views.main, name='main'),
    path('contact', views.contact, name='contact'),
    path('registration', views.registration, name='registration'),
    path('create_user', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('create_add', views.create_add),
    path('delete/<int:add_id>', views.delete_add),
]
