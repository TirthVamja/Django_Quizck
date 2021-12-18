from django.db import models

# Create your models here.
class Player(models.Model):
  gameId=models.CharField(max_length=6)
  username=models.CharField(max_length=15)
  marks=models.TextField(null=True)
  banned=models.BooleanField(default=False)
