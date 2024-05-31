def add_portal_section(request):

    match request.path:
        case p if p.startswith('/courses/'):
            section = 'courses'
        case p if p.startswith('/teacher/'):
            section = 'teacher'
        case p if p.startswith('/user/'):
            section = 'user'
        case _:
            section = 'home'

    return dict(
        section=section,
    )
