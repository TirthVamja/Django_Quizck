from django.shortcuts import render, redirect
from django.core import serializers
from player.models import Player
from host.forms import createQuizForm
from host.models import Quiz, Game, Record
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

## dhvanik firebase
# firebaseConfig = {
#   "apiKey": "AIzaSyCHL_LDHGj7MLqNDOMDhkpxuW_3HPyizAA",
#   "authDomain": "quizck-4548a.firebaseapp.com",
#   "projectId": "quizck-4548a",
#   "storageBucket": "quizck-4548a.appspot.com",
#   "messagingSenderId": "418637328890",
#   "appId": "1:418637328890:web:cf263d4febbff817c63443",
#   "measurementId": "G-WE6D793S4X",
#   "databaseURL":"https://quizck-4548a-default-rtdb.firebaseio.com/"
#   };

import firebase_admin
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="host/templates/firebase.json"

cred=credentials.Certificate('host/templates/firebase.json')
fireapp=firebase_admin.initialize_app(cred,{
  "databaseURL":"https://quizck-74e04-default-rtdb.firebaseio.com/"
},name="game")
dbRef = db.reference()

globReq = ""

def strm(message):
  qz = globReq.session["code"]
  players=""
  try:
    players = Player.objects.filter(banned=False,gameId=qz).values_list('username',flat=True)
  except:
    raise Http404
  alll = []
  for player in players:
    alll.append(player)
  
  return redirect('fbase')

def fbase(req):
  return HttpResponse('<script>window.location="waiting.html";</script>')
  

def waiting(req):
    global globReq
    gameId=""
    try:
      gameId = req.session["code"]
    except:
      raise Http404

    globReq = req
    path='games/'+gameId
    db.reference(path).listen(strm)
    games=""
    try:
      games=list(Game.objects.all())
    except:
      raise Http404
    for x in games:
      if gameId in x.gameId.split(","):
        req.session['hostname']=x.hostname
        req.session['quizId']=x.quizId
        break

    req.session['questionNumber']=0

    try:
      if req.session['user'] == 'player':
        return render(req, 'waiting.html', { 'code': req.session["code"], 'user':req.session['user'], 'playername':req.session['playername']})
      else:
        return render(req, 'waiting.html', { 'code': req.session["code"], 'user':req.session['user']})
    except:
      raise Http404

def showQuiz(req):

  questionNumber=""
  try:
    questionNumber=req.session['questionNumber']+1
  except:
    raise Http404
  req.session['questionNumber']=questionNumber

  try:
    cnt=Quiz.objects.filter(hostname=req.session['hostname'],quizId=req.session['quizId']).count()
    
    if questionNumber>cnt:
      if req.session['user']=="admin":
        return redirect('dashboard')
      else:
        return redirect('join')
    else:
      qz=Quiz.objects.filter(hostname=req.session['hostname'],quizId=req.session['quizId'],questionNumber=questionNumber)[0]
      return render(req,"showQuiz.html",{"quiz":qz})
  except:
    raise Http404

def leaderboard(req):
  answer=req.POST.get('options')
  gameId=req.session['code']
  host=""
  quizId=""
  ques=[]
  try:
    host=req.session['hostname']
    quizId=req.session['quizId']
    ques=list(Quiz.objects.filter(quizId=quizId,questionNumber=req.session['questionNumber'],hostname=host))[0]
  except:
    raise Http404

  
  marks=0
  if ques.answer == answer:
    marks=ques.marks
  try:
    if(req.session['user']=='player'):
      rec=list(Record.objects.filter(gameId=gameId,playername=req.session['playername']))
      if len(rec)==0:
        Record(gameId=gameId, quizId=quizId, marks=str(marks), playername=req.session['playername']).save()
      else:
        rec=rec[0]
        a=rec.marks.split(",")
        if req.session['questionNumber']-1 <= len(a):
          a.append(str(marks))
          a=",".join(a)
          rec.marks=a
          rec.save()
  except:
    raise Http404
  
  players=dbRef.child("games").child(gameId).child("newplayer").get()

  lead=[]
  for i in range(10):
    lead=list(Record.objects.filter(quizId=quizId,gameId=gameId))
    if(len(lead)==len(players)-1):
      flag=False
      for x in lead:
        try:
          if len(x.marks.split(","))!=req.session['questionNumber']:
            flag=True
        except:
          raise Http404
      if not flag:
        break
      else:
        time.sleep(1)
    else:
      time.sleep(1)


  allPlayer=[]
  for item in lead:
    allmarks=item.marks.split(",")
    total=0
    for mrk in allmarks:
      total+=int(mrk)
    if allmarks[len(allmarks)-1]=="0":
      tot=str(total)+' (0)'
    else:
      tot=str(total)+" (+"+str(allmarks[len(allmarks)-1])+")"
    allPlayer.append([total,[item.playername,tot]])
  
  x=allPlayer.sort(reverse=True)
  leader=[y for x,y in allPlayer]
  qz=""
  try:
    qz=Quiz.objects.filter(hostname=req.session['hostname'],quizId=req.session['quizId'],questionNumber=req.session["questionNumber"])[0]
  except:
    raise Http404
  ans=""
  if qz.answer=="1":
    ans=qz.option1
  elif qz.answer=="2":
    ans=qz.option2
  elif qz.answer=="3":
    ans=qz.option3
  elif qz.answer=="4":
    ans=qz.option4
  else:
    raise Http404
  try:
    return render(req,'leaderboard.html',{"leaderboard":leader,"user":req.session['user'],"code":req.session['code'],'quiz':qz,'answer':ans})
  except:
    raise Http404

def download(req,**pk):
  game=""
  gameId=""
  records=""
  questions=""
  try:
    game=pk['game'].split(",")
    gameId,quizId=game
    records=list(Record.objects.filter(gameId=gameId,quizId=quizId))
    questions=list(Quiz.objects.filter(hostname=req.session['username'],quizId=quizId))
  except:
    raise Http404
  
  df = pd.DataFrame()
  df1 = pd.DataFrame()

  ques=[]
  options=[]
  for que in questions:
    x=[]
    y=[]
    x.append(que.question)
    x.append(que.answer)
    x.append(que.marks)
    y.append(que.option1)
    y.append(que.option2)
    y.append(que.option3)
    y.append(que.option4)
    ques.append(x)
    options.append(y)
  
  df['Questions']=[x[0] for x in ques]
  df['Marks']=[x[2] for x in ques]
  ans=[]
  for i in range(len(ques)):
    ans.append(options[i][int(ques[i][1])-1])
  df['Answers']=ans

  lists=[]
  for record in records:
    player=record.playername
    marks=record.marks.split(",")
    total=0
    for x in marks:
      total+=int(x)
    marks.insert(0, player)
    marks.append(total)
    lists.append(marks)
  
  s="Question"
  if lists:
    df1['Player Name']=[x[0] for x in lists]
    for i in range(1,len(lists[0])-1):
      df1[s+str(i)] = [x[i] for x in lists]
    df1['Total Marks']=[x[len(lists[0])-1] for x in lists]
    
    with BytesIO() as b:
        # Use the StringIO object as the filehandle.
        writer = pd.ExcelWriter(b, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Questions')
        df1.to_excel(writer, sheet_name='Marksheet')
        writer.save()
        # Set up the Http response.
        filename = 'django_simple.xlsx'
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

  else:
    raise Http404("No data is found")

def removed(req):
  player=req.session['playername']
  plyr=Player.objects.filter(username=player,gameId=req.session['code'])
  plyr[0].banned=True
  plyr[0].save()
  messages.error(req,"You got Banned !!")
  return redirect('join')