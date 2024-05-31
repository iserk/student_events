import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


# Extending the User model
User.add_to_class('is_student', lambda self: self.groups.filter(name='Students').exists())
User.add_to_class('is_teacher', lambda self: self.groups.filter(name='Teachers').exists())
User.add_to_class('is_enrolled_to', lambda self, course: course.registrations.filter(user=self).exists())
User.add_to_class('can_enroll_to', lambda self, course: course.is_active and not self.is_enrolled_to(course) and course.seats_available() > 0)


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, related_name='owned_courses', on_delete=models.PROTECT)

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    max_seats = models.PositiveIntegerField(null=True, blank=True)

    is_public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def seats_available(self):
        if self.max_seats:
            return self.max_seats - self.registrations.count()
        return None
    def __str__(self):
        return self.title


class CourseRegistration(models.Model):
    user = models.ForeignKey(User, related_name='course_registrations', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='registrations', on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'
