from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('home',views.home,name='home'),
    path('reg',views.reg,name='register'),
    path('post/<int:id>/',views.post,name='post'),
    path('post',views.post,name='post'),
    path('myposts',views.myposts,name='myposts'),
    path('mycomments',views.mycomments,name='mycomments')
]