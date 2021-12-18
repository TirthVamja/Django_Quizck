from django import forms
from .models import Player

class playerForm(forms.ModelForm):
  gameid = forms.CharField()
  username = forms.CharField()
  
  class Meta:
    model = Player
    fields=['gameid','username']