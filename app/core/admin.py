from django.contrib import admin
from . import models


@admin.register(models.CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'registration_date')
    search_fields = ('user__username', 'course__title')
    list_filter = ('registration_date',)
    ordering = ('-registration_date',)

    class Meta:
        unique_together = ('user', 'course')


class CourseRegistrationInline(admin.TabularInline):
    model = models.CourseRegistration
    fields = ('user', 'registration_date')
    readonly_fields = ('registration_date',)
    extra = 0  # No extra empty forms


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'start_date', 'end_date', 'max_seats', 'is_public', 'is_active', 'enrollment_count')
    search_fields = ('title', 'owner__username', 'description')
    list_filter = ('is_public', 'is_active', 'start_date', 'end_date')
    ordering = ('start_date',)
    readonly_fields = ('enrollment_count',)
    inlines = [CourseRegistrationInline, ]

    def seats_available(self, obj):
        return obj.seats_available()

    def enrollment_count(self, obj):
        return obj.registrations.count()

    enrollment_count.short_description = 'Number of enrollments'


