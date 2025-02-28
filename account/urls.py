from django.urls import path, include
from . import views


app_name ='account'

urlpatterns = [
    path('login', views.Login.as_view(), name='login'), 
    path('logout', views.Logout.as_view(), name='logout'), 
    path('signup', views.Signup.as_view(), name='signup'), # サインアップ
]
