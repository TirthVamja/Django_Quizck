from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('',views.login,name='login'),
    path('otp',views.activate,name="otp")
]