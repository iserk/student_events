from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q

from . import models


def request_info(request):
    return render(request, 'core/request_info.html', dict(request=request))

def home(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    #
    return render(request, 'core/home.html')


def show_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'core/profile.html')


def show_course_list(request):
    if request.user.is_authenticated:
        enrolled_courses = Q(registrations__user=request.user)
        public_courses = Q(is_public=True)

        courses = models.Course.objects.filter(public_courses | enrolled_courses).distinct()
    else:
        courses = models.Course.objects.filter(is_public=True)

    return render(request, 'core/course_list.html', dict(courses=courses))


def show_course_detail(request, course_id):
    course = get_object_or_404(models.Course, id=course_id)
    return render(
        request, 'core/course_detail.html',
        dict(
            course=course,
        )
    )

def course_enroll(request, course_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method != 'POST':
        return HttpResponse(status=405)

    course = get_object_or_404(models.Course, id=course_id)

    if not course.is_active:
        messages.error(request, f'The course "{course.title}" is not active.')
        return redirect('course_detail', course_id=course_id)

    if not request.user.can_enroll_to(course):
        messages.error(request, f'You are not allowed to enroll in the course "{course.title}".')
        return redirect('course_detail', course_id=course_id)

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


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')



def teacher_course_list(request):
    courses = models.Course.objects.filter(owner=request.user)
    return render(request, 'core/teacher_course_list.html', dict(courses=courses))


def teacher_student_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_teacher:
        messages.error(request, 'You must be a teacher to view this page.')
        return redirect('home')

    students = models.User.objects.filter(groups__name='Students')
    print(students)
    return render(request, 'core/students_activity.html', dict(students=students))


def teacher_course_detail(request, course_id):
    course = get_object_or_404(models.Course, id=course_id)

    if request.user != course.owner:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('home')

    return render(
        request, 'core/teacher_course_detail.html',
        dict(
            course=course,
        )
    )


def teacher_course_update(request, course_id):
    if request.method != 'POST':
        return HttpResponse(status=405)

    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to update a course.')
        return redirect('login')

    course = get_object_or_404(models.Course, id=course_id)

    if not request.user.is_teacher or request.user != course.owner:
        messages.error(request, "You are not authorized to update this course.")
        return redirect('course_detail', course_id=course_id)

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
