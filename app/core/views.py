from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from . import models


def home(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    #
    return render(request, 'core/home.html', dict(section='home'))


def show_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'core/profile.html', dict(section='user'))

def show_course_list(request):
    courses = models.Course.objects.filter(is_public=True)
    return render(request, 'core/course_list.html', dict(courses=courses, section='courses'))


def show_course_detail(request, course_id):
    course = get_object_or_404(models.Course, id=course_id)
    return render(request, 'core/course_detail.html', dict(course=course, section='courses'))


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('home')  # Redirect to a home page or any other page
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', dict(form=form, section='user'))


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')