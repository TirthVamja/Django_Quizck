from django.db import models
# Create your models here.

class Quiz(models.Model):
    hostname=models.CharField(max_length=15)
    quizId=models.IntegerField()
    questionNumber=models.IntegerField()
    question=models.CharField(max_length=500)
    option1=models.CharField(max_length=100)
    option2=models.CharField(max_length=100)
    option3=models.CharField(max_length=100)
    option4=models.CharField(max_length=100)
    answer=models.CharField(max_length=5)
    marks=models.IntegerField()
    timer=models.IntegerField()


# For storing the result records of student
class Record(models.Model):
  gameId=models.CharField(max_length=10)
  quizId=models.IntegerField()
  marks=models.TextField()
  playername=models.CharField(max_length=50)

# To handle many occurences of same quiz
class Game(models.Model):
  hostname=models.CharField(max_length=100)
  quizId=models.IntegerField()
  gameId=models.TextField()
  gameTime=models.TextField()

  # gameTime=ArrayField(models.DateTimeField(),default=list)