from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from . import models


def request_info(request):
    return render(request, 'core/request_info.html', dict(request=request))

def home(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    #
    groups = request.user.groups.all()
    is_teacher = groups.filter(name='Teachers').exists()
    is_student = groups.filter(name='Students').exists()

    if not is_teacher and is_student:
        return redirect('student_home')
    elif is_teacher and not is_student:
        return redirect('teacher_home')
    else:
        return render(request, 'core/home.html', dict(section='home', portal='home'))


def student_home(request):
    return render(request, 'core/student_home.html', dict(section='home', portal='student'))


def teacher_home(request):
    return render(request, 'core/teacher_home.html', dict(section='home', portal='teacher'))


def show_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'core/profile.html', dict(section='user'))

def show_course_list(request):
    courses = models.Course.objects.filter(is_public=True)
    return render(request, 'core/course_list.html', dict(courses=courses, section='courses'))


def show_course_detail(request, course_id):
    course = get_object_or_404(models.Course, id=course_id)
    return render(request, 'core/course_detail.html',
                  dict(
                      course=course,
                      section='courses',
                      is_enrolled=request.user.is_authenticated and request.user.course_registrations.filter(course=course).exists(),
                      can_enroll=request.user.is_authenticated and not request.user.course_registrations.filter(course=course).exists() and course.seats_available() > 0
                  ))

def course_enroll(request, course_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method != 'POST':
        return HttpResponse(status=405)

    course = get_object_or_404(models.Course, id=course_id)
    registration, created = models.CourseRegistration.objects.get_or_create(user=request.user, course=course)
    if created:
        messages.success(request, f'You have successfully enrolled in the course "{course.title}".')
    else:
        messages.error(request, f'You are already enrolled in the course "{course.title}".')
    return redirect('course_detail', course_id=course_id)


def course_unenroll(request, course_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method != 'POST':
        return HttpResponse(status=405)

    course = get_object_or_404(models.Course, id=course_id)
    registration = get_object_or_404(models.CourseRegistration, user=request.user, course=course)
    registration.delete()
    messages.success(request, f'You have successfully unenrolled from the course "{course.title}".')
    return redirect('course_detail', course_id=course_id)


def teacher_course_list(request):
    courses = models.Course.objects.filter(owner=request.user)
    return render(request, 'core/teacher_course_list.html', dict(courses=courses, section='courses'))


def teacher_course_detail(request, course_id):
    course = get_object_or_404(models.Course, id=course_id)
    return render(request, 'core/teacher_course_detail.html',
                  dict(
                      course=course,
                      section='courses',
                      is_enrolled=request.user.is_authenticated and request.user.course_registrations.filter(course=course).exists(),
                      can_enroll=request.user.is_authenticated and not request.user.course_registrations.filter(course=course).exists() and course.seats_available() > 0
                  ))

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


def teacher_course_update(request, course_id):
    if request.method != 'POST':
        return HttpResponse(status=405)

    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to update a course.')
        return redirect('login')

    course = get_object_or_404(models.Course, id=course_id)

    if not request.user.is_teacher or request.user != course.owner:
        messages.error(request, "You are not authorized to update this course.")
        return redirect('teacher_home')

    if request.POST.get('active'):
        new_status = True if request.POST.get('active') == '1' else False
        course.is_active = new_status
        course.save()
        messages.success(request, f'The course "{course.title}" active status has been changed to {new_status}')

    if request.POST.get('public'):
        new_status = True if request.POST.get('public') == '1' else False
        course.is_public = new_status
        course.save()
        messages.success(request, f'The course "{course.title}" published status has been changed to {new_status}')

    return redirect('teacher_course_detail', course_id=course_id)