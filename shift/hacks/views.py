from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import ShiftPostForm, ShifterProfileForm
from .models import Shift_post



def home(request):
    if request.user.is_authenticated:
        # should be changed eventually to show the specific user's feed
        shift_posts = Shift_post.objects.all()
        if request.method == 'POST':
            ns_form = ShiftPostForm(request.POST)
            if ns_form.is_valid():
                post = ns_form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('home')
        else:
            ns_form = ShiftPostForm()
        return render(request, 'hacks/myhome.html', {'shift_posts': shift_posts, 'ns_form': ns_form})

    l_form = AuthenticationForm()
    r_form = UserCreationForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            l_form = AuthenticationForm(request, request.POST)
            if l_form.is_valid():
                user = l_form.get_user()
                login(request, user)
                l_form = AuthenticationForm()
                return redirect('profile')
            else:
                print(l_form.errors)
        elif 'register_submit' in request.POST:
            r_form = UserCreationForm(request.POST)
            if r_form.is_valid():
                user = r_form.save()
                login(request, user) 
                l_form = UserCreationForm()
                return redirect('profile')
            else:
                print(r_form.errors)

    shift_posts = Shift_post.objects.all()
    return render(request, 'hacks/home.html', {'shift_posts': shift_posts, 'l_form': l_form, 'r_form': r_form})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


def profile(request):
    user = request.user

    if request.method == 'POST':
        pe_form = ShifterProfileForm(request.POST, instance=user)
        if pe_form.is_valid():
            pe_form.save()
            return redirect('profile')
        else:
            print(pe_form.errors)
    else:
        pe_form = ShifterProfileForm(instance=user)

    shift_posts = Shift_post.objects.all()
    return render(request, 'hacks/profile.html', {'shift_posts': shift_posts, 'pe_form': pe_form})