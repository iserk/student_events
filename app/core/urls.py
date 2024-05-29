from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("courses/", views.show_course_list, name="course_list"),
    path("courses/<uuid:course_id>/", views.show_course_detail, name="course_detail"),
]
