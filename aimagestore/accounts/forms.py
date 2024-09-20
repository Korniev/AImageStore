from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import PasswordInput, CharField, EmailField, TextInput, EmailInput, Form
from .models import User
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    username = CharField(
        max_length=100,
        min_length=3,
        required=True,
        widget=TextInput(attrs={"class": "data-input"}),
        error_messages={
            'required': _("Username is required."),
            'min_length': _("Username must be at least 3 characters long."),
        }
    )
    email = EmailField(
        max_length=100,
        required=True,
        widget=EmailInput(attrs={"class": "data-input"}),
        error_messages={
            'required': _("Email is required."),
            'invalid': _("Enter a valid email address."),
        }
    )
    password1 = CharField(
        required=True,
        widget=PasswordInput(attrs={"class": "data-input"}),
        error_messages={
            'required': _("Password is required."),
        }
    )
    password2 = CharField(
        required=True,
        widget=PasswordInput(attrs={"class": "data-input"}),
        error_messages={
            'required': _("Confirm your password."),
            'password_mismatch': _("Passwords do not match."),
        }
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("This email is already in use!"))
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError(_("This field is required."))
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        username = self.cleaned_data.get("username")

        if len(password1) < 8:
            raise ValidationError(_("This password is too short. It must contain at least 8 characters!"))
        if password1.isdigit():
            raise ValidationError(_("This password must contain at least one character that is not a digit!"))
        if username.lower() in password1.lower():
            raise ValidationError(_("The password is too similar to the username!"))
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("The two password fields didn’t match."))
        return password2


class LoginForm(AuthenticationForm):
    email = EmailField(max_length=100, required=True, widget=EmailInput(attrs={"class": "data-input"}))
    password = CharField(required=True, widget=PasswordInput(attrs={"class": "data-input"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise ValidationError('Invalid email or password.')

        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class ChangePasswordForm(Form):
    new_password = CharField(label='New password', widget=PasswordInput(attrs={"class": "data-input"}))
    confirm_new_password = CharField(label='Confirm new password', widget=PasswordInput(attrs={"class": "data-input"}))
