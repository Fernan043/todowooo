from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError #preguntar porque
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
# Create your views here.


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
         return render(request, 'todo/signupuser.html',{'form':UserCreationForm()})
    else:
        #Create a new user
        if request.POST['password1'] == request.POST['password2']:
           try:
            user=User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('currenttodos')
           except IntegrityError:
               return render(request, 'todo/signupuser.html',{'form':UserCreationForm(), 'error':'That username is currently in use'})
        else:
            return render(request, 'todo/signupuser.html',{'form':UserCreationForm(), 'error':'Passwords did not match'})


def currenttodos(request):
    #esta linea declara que solo jale los todo de el usuario en especifico para que los que no correspondan a el no sea visibles
    todos= Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html',{'todos':todos})


def logoutuser(request):
    #este post es basicamente porque sin el despues de un login el navegador nos hecharia ya que tiene precargada dicha accion o pagina
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
def loginuser(request):
    if request.method == 'GET':
         return render(request, 'todo/loginuser.html',{'form':AuthenticationForm})
    else:
        user=authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',{'form':AuthenticationForm,'error':'Username and password incorrect'})
        else:
            login(request, user)
            return redirect('currenttodos')
        

def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html',{'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            #la linea de abajo evita que se guarde en la base de datos sin antes una autorizacion el false es la clave como tal, sino se guardaria de manera automatica en BD
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html',{'form':TodoForm(),'error':'Bad data pass in'})