from django.shortcuts import render, redirect
from django.core import serializers
from player.models import Player
from .forms import createQuizForm
from .models import Quiz, Game, Record
from django.http import HttpResponse, Http404
import json
import shortuuid
import firebase_admin
from firebase_admin import db, credentials
import datetime,pytz
import time
from io import BytesIO
import pandas as pd
from django.contrib import messages

# mihir firebase
firebaseConfig = {
  "apiKey": "AIzaSyDNn1-wkMm-g0cH2BKQ6XjdLTl6ldds8ZE",
  "authDomain": "quizck-74e04.firebaseapp.com",
  "projectId": "quizck-74e04",
  "storageBucket": "quizck-74e04.appspot.com",
  "messagingSenderId": "555502389734",
  "appId": "1:555502389734:web:2a977e89e54df3c69cae27",
  "measurementId": "G-XFLZV89Q56",
  "databaseURL": "https://quizck-74e04-default-rtdb.firebaseio.com/"
}

import firebase_admin
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="host/templates/firebase.json"

cred=credentials.Certificate('host/templates/firebase.json')
fireapp=firebase_admin.initialize_app(cred,{
  "databaseURL":"https://quizck-74e04-default-rtdb.firebaseio.com/"
},name="host")
dbRef = db.reference()


def dashboard(req):
  username=""
  quiz=""
  try:
    username = req.session['username']
    quiz = Quiz.objects.filter(hostname=username).values_list('quizId', flat=True).distinct()
  except:
    raise Http404
      
  quizzes = []
  i = 1
  for x in quiz:
      quizzes.append([i, x])
      i += 1
  return render(req, 'dashboard.html', {'quizzes': quizzes})


def quiz(req):
  username=""
  temp=""
  try:
    username = req.session['username']
    temp = Quiz.objects.filter(hostname=username).values_list('quizId',flat=True)
  except:
    raise Http404
  mx = 0
  for x in temp:
    mx = max(mx, x)
  req.session['quizId'] = mx + 1
  return redirect('createQuiz')


def createQuiz(req):
    if req.method == 'POST':
        form = createQuizForm(req.POST)
        if form.is_valid():
          cnt=""
          try:
            cnt=Quiz.objects.filter(quizId=req.session['quizId'],hostname=req.session['username']).count()
          except:
            raise Http404
          questionNumber = cnt+1
          question = req.POST['question']
          option1 = req.POST['option1']
          option2 = req.POST['option2']
          option3 = req.POST['option3']
          option4 = req.POST['option4']
          answer = req.POST['answer']
          marks = req.POST['marks']
          timer = req.POST['timer']

          username = req.session['username']
          quizId = req.session['quizId']

          quiz = Quiz(hostname=username,
                      quizId=quizId,
                      questionNumber=questionNumber,
                      question=question,
                      option1=option1,
                      option2=option2,
                      option3=option3,
                      option4=option4,
                      answer=answer,
                      marks=marks,
                      timer=timer)

          quiz.save()
          form = createQuizForm()
    else:
        form = createQuizForm()

    return render(req, 'createQuiz.html', {'form': form})


def done(req):
    if req.method == 'POST':
      form = createQuizForm(req.POST)
      if form.is_valid():
        cnt=''
        try:
          cnt=Quiz.objects.filter(quizId=req.session['quizId'],hostname=req.session['username']).count()
        except:
          raise Http404
        questionNumber = cnt+1
        question = req.POST['question']
        option1 = req.POST['option1']
        option2 = req.POST['option2']
        option3 = req.POST['option3']
        option4 = req.POST['option4']
        answer = req.POST['answer']
        marks = req.POST['marks']
        timer = req.POST['timer']

        username = req.session['username']
        quizId = req.session['quizId']

        quiz = Quiz(hostname=username,quizId=quizId,questionNumber=questionNumber,question=question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer,marks=marks,timer=timer)

        quiz.save()

    return redirect('dashboard')
    
def stats(req, **primarykey):
  quizId=primarykey['pk']
  game=""
  hostname=""
  try:
    hostname=req.session['username']
    game=list(Game.objects.filter(hostname=hostname,quizId=quizId))
  except:
    raise Http404
  if not game:
    return render(req,'stats.html',{"quizId":quizId,"games":[]})
  game=game[0]
  gameIds=game.gameId.split(",")
  gameTimes=game.gameTime.split(",")
  games=[]
  for i in range(len(gameIds)):
    games.append([gameIds[i],gameTimes[i]])

  games.sort(key = lambda x: x[1])
  games.reverse()
  return render(req,'stats.html',{"games":games,"quizId":quizId})

def quizPage(req, **primarykey):
    quizId = primarykey['pk']
    qz=""
    try:
      qz = Quiz.objects.filter(quizId=quizId, hostname=req.session["username"])
    except:
      raise Http404
    qz = serializers.serialize('json', qz)
    qz = json.loads(qz)
    code = shortuuid.ShortUUID().random(length=4)
    req.session["code"] = code
    req.session['user']="admin"
    req.session['quizId']=quizId
    
    game=""
    dt=""
    quizId=""
    username=""
    try:
      username = req.session['username']
      quizId = req.session['quizId']
      dt=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
      
      game=list(Game.objects.filter(hostname=username,quizId=quizId))
    except:
      raise Http404

    if len(game)==0:
      game=Game(hostname=username,quizId=quizId,gameId=code,gameTime=dt.strftime("%b %d %Y %H:%M:%S"))
      game.save()
    else:
      game=game[0]
      gameId=game.gameId.split(",")
      gameTime=game.gameTime.split(",")
      gameId.append(code)
      gameTime.append(dt.strftime("%b %d %Y %H:%M:%S"))
      game.gameId=",".join(gameId)
      game.gameTime=",".join(gameTime)
      game.save()

    dbRef.child("games").child(code).set({
      'host': req.session["username"],
      'next': 0,
      'newplayer': [''],
      'started':0
    })
    return redirect('waiting')

def logout(req):
  for key in list(req.session.keys()):
    if not key.startswith("_"):
      del req.session[key]

  return redirect('login')