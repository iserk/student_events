from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path("learn/", views.student_home, name="student_home"),
    path("learn/courses/", views.show_course_list, name="course_list"),
    path("learn/courses/<uuid:course_id>/", views.show_course_detail, name="course_detail"),
    path("learn/courses/<uuid:course_id>/enroll/", views.course_enroll, name="course_enroll"),
    path("learn/courses/<uuid:course_id>/unenroll/", views.course_unenroll, name="course_unenroll"),

    path("teach/", views.teacher_home, name="teacher_home"),
    path("teach/courses/", views.teacher_course_list, name="teacher_course_list"),
    path("teach/courses/<uuid:course_id>/", views.teacher_course_detail, name="teacher_course_detail"),
    path("teach/courses/<uuid:course_id>/update/", views.teacher_course_update, name="teacher_course_update"),

    path('user/login/', views.user_login, name='login'),
    path('user/logout/', views.user_logout, name='logout'),
    # path('user/forgot/', views.user_forgot, name='forgot'),
    # path('user/signup/', views.user_signup, name='signup'),
    path('user/profile/', views.show_profile, name='profile'),
]
