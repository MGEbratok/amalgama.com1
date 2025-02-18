from django.urls import path
from django.contrib.auth import views as standart_views

from . import views

urlpatterns =[
    path("reg/", views.register ,name = "register"),
    path("", views.main, name = "home"),
    path("reg/", views.register, name = "register"),   
    path("email_confirmation/<email>", views.email_confirmation, name = "email_confirmation"),
    path("login/", standart_views.LoginView.as_view(), name="login"),
    path("logout/", standart_views.LogoutViews.as_view(), name= "logout"),
    path('find-users/', views.find_users, name='find_users'), 
]