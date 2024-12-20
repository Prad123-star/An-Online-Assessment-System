from django.urls import  path

from . import views

urlpatterns=[
       path('saveUser/',views.saveUser),
       path('login/',views.login)
]