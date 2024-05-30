from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path("courses/", views.show_course_list, name="course_list"),
    path("courses/<uuid:course_id>/", views.show_course_detail, name="course_detail"),
    path("courses/<uuid:course_id>/enroll/", views.course_enroll, name="course_enroll"),
    path("courses/<uuid:course_id>/unenroll/", views.course_unenroll, name="course_unenroll"),

    path('user/login/', views.user_login, name='login'),
    path('user/logout/', views.user_logout, name='logout'),
    # path('user/forgot/', views.user_forgot, name='forgot'),
    # path('user/signup/', views.user_signup, name='signup'),
    path('user/profile/', views.show_profile, name='profile'),
]
