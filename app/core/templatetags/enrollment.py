from django.urls import reverse

from django import template

register = template.Library()

@register.filter
def is_enrolled_to(user, course):
    return user.is_enrolled_to(course)


@register.filter
def can_enroll_to(user, course):
    return user.can_enroll_to(course)


@register.filter
def absolute_uri(url, request):
    return request.build_absolute_uri(url)


@register.simple_tag(takes_context=True)
def full_url(context, view_name, *args, **kwargs):
    request = context['request']
    relative_url = reverse(view_name, args=args, kwargs=kwargs)
    return request.build_absolute_uri(relative_url)