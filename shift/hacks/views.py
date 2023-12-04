from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import ShiftPostForm
from .models import Shift_post



def home(request):
    if request.user.is_authenticated:
        # should be changed eventually to show the specific user's feed
        shift_posts = Shift_post.objects.all()
        return render(request, 'hacks/myhome.html', {'shift_posts': shift_posts})
    shift_posts = Shift_post.objects.all()
    return render(request, 'hacks/home.html', {'shift_posts': shift_posts})


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = UserCreationForm()
    
    return render(request, 'hacks/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'hacks/login.html', {'form': form})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


def profile(request):
    return render(request, 'hacks/profile.html')


def new_shift(request):
    if request.method == 'POST':
        form = ShiftPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = ShiftPostForm()

    return render(request, 'hacks/newshift.html', {'form': form})