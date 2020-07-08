from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='threeindex'),
    path('whoami', views.whoami, name='whoami'),
    path('get_auth_code', views.get_auth_code, name='get_auth_code'),
    path('get_access_token', views.get_access_token, name='get_access_token')
]