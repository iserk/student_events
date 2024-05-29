from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from . import models

def index(request):
    name = 'World :)'
    return HttpResponse(f"Hello, {name}! You're at the core index.")


def show_course_list(request):
    courses = models.Course.objects.filter(is_public=True)
    return render(request, 'core/course_list.html', {'courses': courses})


def show_course_detail(request, course_id):
    course = get_object_or_404(models.Course, id=course_id)
    return render(request, 'core/course_detail.html', {'course': course})