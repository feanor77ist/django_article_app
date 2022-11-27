from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

# Create your views here.

def register(request):
    form = RegisterForm(request.POST or None)
    
    if form.is_valid(): 
          
        username = form.cleaned_data.get("username")        
        # Kullanıcı adı kontrolü
        for i in User.objects.all():
            if i.username == username:
                messages.warning(request, username + " Kullanıcısı Sistemde Kayıtlı!")
                context = {
                    "form": form
                    }
                return render(request, "article/register.html", context) 
        
        password = form.cleaned_data.get("password")
        newUser = User(username = username)
        newUser.set_password(password)
        newUser.save()
        login(request, newUser)
        messages.success(request, "Başarıyla Kayıt Oldunuz...")
        return redirect("index")

    context = {
        "form": form
        }
    return render(request, "article/register.html", context)    

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        if user is None:
            messages.warning(request, "Kullanıcı adı veya parola hatalı!")
            return render(request, "article/login.html", context)
        messages.success(request, "Başarıyla Giriş Yaptınız")
        login(request, user)
        return redirect("index")
    return render(request, "article/login.html", context)


def logoutUser(request):
    logout(request)
    messages.success(request, "Başarıyla Çıkış Yaptınız")
    return redirect("index")
