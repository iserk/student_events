def add_portal_section(request):
    portal = 'student' if request.path.startswith('/learn/') else 'teacher' if request.path.startswith('/teach/') else 'home'

    match request.path:
        case p if p.startswith('/learn/courses/'):
            section = 'courses'
        case p if p.startswith('/teach/courses/'):
            section = 'manage_courses'
        case _:
            section = 'home'

    return dict(
        portal=portal,
        section=section,
    )
