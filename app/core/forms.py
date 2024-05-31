from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    # Stylize the login form using Bootstrap 5
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password'].widget.render_value = False
