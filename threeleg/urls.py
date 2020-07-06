from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='threeindex'),
    path('whoami', views.whoami, name='whoami')
]