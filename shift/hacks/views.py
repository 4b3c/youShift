from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import ShifterCreationForm, UsernameAuthenticationForm, ShiftPostForm, ShifterProfileForm
from .models import Shift_post

import os
from django.conf import settings


def home(request):
    if request.user.is_authenticated:
        # should be changed eventually to show the specific user's feed
        shift_posts = Shift_post.objects.all()
        print(shift_posts[0].id)
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

    l_form = UsernameAuthenticationForm()
    r_form = ShifterCreationForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            l_form = UsernameAuthenticationForm(request, request.POST)
            if l_form.is_valid():
                user = l_form.get_user()
                login(request, user)
                l_form = UsernameAuthenticationForm()
                return redirect('profile')
            else:
                print(l_form.errors)
        elif 'register_submit' in request.POST:
            r_form = ShifterCreationForm(request.POST)
            if r_form.is_valid():
                user = r_form.save()
                login(request, user) 
                r_form = ShifterCreationForm()
                return redirect('profile')
            else:
                print("R_Form Errors: ", r_form.errors, "\nRequest POST: ", request.POST)

    shift_posts = Shift_post.objects.all()
    return render(request, 'hacks/home.html', {'shift_posts': shift_posts, 'l_form': l_form, 'r_form': r_form})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


def profile(request):
    user = request.user

    if request.method == 'POST':
        pe_form = ShifterProfileForm(request.POST, request.FILES, instance=user)
        if pe_form.is_valid():
            profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pics')
            filename = f'{user.username}.jpg'
            print("REQUEST.FILES: ", request.FILES)
            if request.FILES == {}:
                with open(os.path.join(profile_pics_dir, filename), 'rb') as f:
                    uploaded_img = f.read()
            else:
                uploaded_img = request.FILES['profile_picture'].read()

            if not os.path.exists(profile_pics_dir):
                os.makedirs(profile_pics_dir)

            with open(os.path.join(profile_pics_dir, filename), 'wb+') as f:
                f.write(uploaded_img)

            user.profile_picture = os.path.join('profile_pics', filename)
            pe_form.save()
            return redirect('profile')
        else:
            print(pe_form.errors)
    else:
        pe_form = ShifterProfileForm(instance=user)

    shift_posts = Shift_post.objects.all()
    return render(request, 'hacks/profile.html', {'shift_posts': shift_posts, 'pe_form': pe_form})




def post(request, post_id):
    post = get_object_or_404(Shift_post, pk=post_id)
    return render(request, 'hacks/post.html', {'post': post})