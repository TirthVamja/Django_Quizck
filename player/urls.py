from django.urls import path
from . import views

urlpatterns = [
    path('join/',views.joinplayer,name='join'),
]