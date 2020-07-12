from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getusers', views.getusers, name='getusers'),
    path('learnlogout', views.learnlogout, name='learnlogout')
]