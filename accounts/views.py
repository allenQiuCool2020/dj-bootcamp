
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import LoginForm, RegisterForm
from django.core.exceptions import ValidationError

User = get_user_model()

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")  
       
        if password != password2:
            raise ValidationError("Your password does not equal to confirm password")     

        else:
            try:
                user = User.objects.create_user(username, email, password)
            except:
                user = None
            if user != None:
                # user is valid and active -> is_active
                # request.user = user
                login(request, user)
                return redirect("/")
            else:
                request.session['register_error'] = 1 # 1 == True
        
    return render(request, "forms.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user != None:
            # user is valid and active -> is_active
            # request.user = user
            login(request, user)
            return redirect("/")
        else:

            # attempt = request.session.get("attempt") or 0
            # print(attempt)
            # request.session['attempt'] += 1 
            request.session['invalid_user'] = 1 # 1 == True
        
    return render(request, "forms.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("/login")