from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import RegisterationForm, LoginForm

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = form.errors.as_text()
            if 'password2' in form.errors:
                error_message = "Passwords do not match."
            elif 'email' in form.errors:
                error_message = "Email is already in use or invalid."
            return render(request, 'user/register.html', {'form': RegisterationForm(), "errors": error_message})
    return render(request, 'user/register.html', {'form': RegisterationForm()})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'user/login.html', {'form': form, 'errors': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

