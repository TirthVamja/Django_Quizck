from django.http import HttpResponse,Http404
from django.shortcuts import render,redirect
from .forms import signupForm,loginForm
from .models import Login
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from Crypto.Cipher import AES
from django.core.mail import EmailMessage
import shortuuid
from mysite import settings

@csrf_exempt 
def signup(request):
  username=""
  emailId=""
  password=""
  if request.method == 'POST':
      form = signupForm(request.POST)
      if form.is_valid():
        username=request.POST['username']
        password=request.POST['password']
        emailId=request.POST['emailId']
        
        checking=Login.objects.filter(username=username)
        if checking.exists():
          messages.error(request,'Username already exists !!')
          return render(request, 'signup.html', {'form': form})
        
        obj = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
        password=obj.encrypt(password)

        userLogin=Login(username=username,password=password,emailId=emailId)
        userLogin.save()

        return redirect('login')
  else:
      form = signupForm()

  return render(request, 'signup.html', {'username': username,"password":password,"emailId":emailId})

def login(request):
  username=""
  password=""
  if request.method == 'POST':
      form = loginForm(request.POST)
      if form.is_valid():
        username=request.POST['username']
        password=request.POST['password']
        
        obj = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
        passw=obj.encrypt(password)

        checking=Login.objects.filter(username=username,password=passw)
        if checking.exists():
          request.session['username']=username
          return redirect('dashboard')
        else:
          messages.error(request,'Incorrect Username or Password')
  else:
      form = loginForm()

  return render(request, 'login.html', {'username': username,"password":password})

def activate(req):
  if req.method == 'POST':
    try:
      email=req.POST['email']
      email_subject = "Confirm your Email for Quizck!!"
      otp = shortuuid.ShortUUID().random(length=4)
      message2 = "Please Enter this OTP "+otp
      email = EmailMessage(
          email_subject,
          message2,
          settings.EMAIL_HOST_USER,
          [email],
      )
      email.fail_silently = True
      email.send()
    except:
      messages.error(req,"Enter the email First")
      return redirect('signup')
  else:
    raise Http404

# gAAAAABhdSHHTU5MBmsOxehQ5LxBKb2eWq3ckaBWEnk6VIfyGDPgQZxnMNDUacwI2pVEq-RDT6mkzCi55hNyPDKlclyXzWH9DA==

# gAAAAABhdSFDXdT3_aGlMX2FPN0UJ8QL6JJkrPYnOJtklqE0TUZUQ51nzqI_uyzVV4vxEICgPx16YED-0Z7xviYXLgX3wTKrTw==

# b'\xe5\xc2?g\x9fE{\x7f|\xcdm-$'
# b'\xe5\xc2?g\x9fE{\x7f|\xcdm-$'





