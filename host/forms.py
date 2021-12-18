from django import forms
from .models import Quiz

class createQuizForm(forms.ModelForm):
  CHOICES=(('1','1'),('2','2'),('3','3'),('4','4'))
  
  
  question=forms.CharField(max_length=500)
  option1=forms.CharField(max_length=100)
  option2=forms.CharField(max_length=100)
  option3=forms.CharField(max_length=100)
  option4=forms.CharField(max_length=100)
  answer=forms.ChoiceField(choices = CHOICES)
  marks=forms.IntegerField()
  timer=forms.IntegerField()
  class Meta:
    model = Quiz
    fields=['question','option1','option2','option3','option4','answer','marks','timer']