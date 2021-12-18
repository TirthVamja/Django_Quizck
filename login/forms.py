from django import forms
from django.forms import fields
from django.forms.widgets import EmailInput
from .models import Login

class loginForm(forms.ModelForm):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)
  
  class Meta:
    model = Login
    fields=['username','password']

class signupForm(forms.ModelForm):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)
  emailId = forms.CharField(widget=EmailInput)
  class Meta:
    model = Login
    fields=['username','password','emailId']