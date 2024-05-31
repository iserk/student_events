from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views, forms


urlpatterns = [
    path("", views.home, name="home"),

    path("request-info/", views.request_info, name="request_info"),

    path("courses/", views.show_course_list, name="course_list"),
    path("courses/<uuid:course_id>/", views.show_course_detail, name="course_detail"),
    path("courses/<uuid:course_id>/enroll/", views.course_enroll, name="course_enroll"),
    path("courses/<uuid:course_id>/unenroll/", views.course_unenroll, name="course_unenroll"),

    path("teacher/courses/", views.teacher_course_list, name="teacher_course_list"),
    path("teacher/students/", views.teacher_student_list, name="teacher_student_list"),
    path("teacher/courses/<uuid:course_id>/", views.teacher_course_detail, name="teacher_course_detail"),
    path("teacher/courses/<uuid:course_id>/update/", views.teacher_course_update, name="teacher_course_update"),

    # path('user/login/', views.user_login, name='login'),

    path(
        'user/login/',
        LoginView.as_view(
            template_name="core/login.html", #this is default, change as needed
            authentication_form=forms.LoginForm,
        ),
        name='login'
    ),

    path('user/logout/', views.user_logout, name='logout'),
    # path('user/forgot/', views.user_forgot, name='forgot'),
    # path('user/signup/', views.user_signup, name='signup'),
    path('user/profile/', views.show_profile, name='profile'),
]
