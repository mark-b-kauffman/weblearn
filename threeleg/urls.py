from django.urls import path
from . import views

urlpatterns = [
    path('', views.threeindex, name='threeindex'),
    path('whoami', views.whoami, name='whoami'),
    path('courses', views.courses, name='courses'),
    path('get_auth_code', views.get_auth_code, name='get_auth_code'),
    path('get_access_token', views.get_access_token, name='get_access_token')
]