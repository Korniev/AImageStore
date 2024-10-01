from datetime import datetime

import pyotp
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import User
from .forms import RegisterForm, LoginForm, ChangePasswordForm
from .utils import send_otp, set_language

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.utils import timezone
from datetime import timedelta


def login_view(request):
    user = request.user
    lang_code = set_language(request)

    if user.is_authenticated:
        return HttpResponse(_("You are already logged in as {username}.").format(username=user.username))

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_verified:
                    login(request, user)
                    return redirect(f"{reverse('main')}?lang={lang_code}")
                else:
                    request.session['email'] = email
                    send_otp(request, email)
                    messages.error(request, _("Please verify your email."))
                    return redirect(f"{reverse('accounts:code-verification')}?lang={lang_code}")
        else:
            print(form.errors)
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form, 'lang_code': lang_code})


def register_view(request, *args, **kwargs):
    user = request.user
    lang_code = set_language(request)

    if user.is_authenticated:
        return HttpResponse(_("You are already logged in as {username}.").format(username=user.username))

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            request.session['email'] = email
            send_otp(request, email)
            return redirect(f"{reverse('accounts:code-verification')}?lang={lang_code}")
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, "accounts/register.html", context)


def code_verification_view(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp_digit')
        print(otp_code)
        email = request.session.get('email')
        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_date = request.session.get('otp_valid_date')
        type = request.session.get('type')

        if otp_secret_key and otp_valid_date is not None:
            valid_date = datetime.fromisoformat(otp_valid_date)
            if datetime.now() < valid_date:
                totp = pyotp.TOTP(otp_secret_key, interval=300)
                if totp.verify(otp_code):
                    try:
                        user = User.objects.get(email=email)
                        user.is_verified = True
                        user.save()

                        del request.session['otp_secret_key']
                        del request.session['otp_valid_date']
                        if type == 'new-password':
                            return redirect(f"{reverse('accounts:new-password')}?lang={set_language(request)}")
                        else:
                            messages.success(request,
                                             _("Congratulations {username}! You have verified your email.").format(
                                                 username=user.username))
                            return redirect(f"{reverse('accounts:login')}?lang={set_language(request)}")
                    except User.DoesNotExist:
                        messages.error(request, _("User with this email was not found."))
                        return redirect(f"{reverse('accounts:register')}?lang={set_language(request)}")
                else:
                    messages.error(request, _("Your code is incorrect."))
                    return redirect(f"{reverse('accounts:code-verification')}?lang={set_language(request)}")

            else:
                messages.error(request, _("Your code is no longer valid."))
                return redirect(f"{reverse('accounts:code-verification')}?lang={set_language(request)}")

    return render(request, "accounts/code-verification.html")


def resend_otp(request):
    if request.method == 'POST':
        email = request.session.get('email')
        if email:
            send_otp(request, email)  # Відправити новий OTP код
            messages.success(request, _("A new code has been sent."))
        else:
            messages.error(request, _("User with this email was not found."))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def email_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            request.session['email'] = email
            request.session['type'] = "new-password"
            send_otp(request, email)
            return redirect(f"{reverse('accounts:code-verification')}?lang={set_language(request)}")
        except User.DoesNotExist:
            messages.error(request, _("User with this email was not found."))
            return redirect(f"{reverse('accounts:email')}?lang={set_language(request)}")
    return render(request, "accounts/email.html")


def change_password_view(request):
    email = request.session.get('email')
    try:
        user = User.objects.get(email=email)
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                confirm_new_password = form.cleaned_data['confirm_new_password']
                if new_password == confirm_new_password:
                    user.password = make_password(new_password)
                    user.save()
                    messages.success(request, _("Your password has been successfully changed."))
                    return redirect(f"{reverse('accounts:login')}?lang={set_language(request)}")
                else:
                    form.add_error('confirm_new_password', _("Passwords do not match."))
        else:
            form = ChangePasswordForm()
    except User.DoesNotExist:
        messages.error(request, _("User with this email was not found."))
        return redirect(f"{reverse('accounts:email')}?lang={set_language(request)}")
    return render(request, 'accounts/new-password.html', {'form': form})


def logout_view(request):
    lang_code = set_language(request)

    logout(request)
    messages.add_message(request, messages.SUCCESS, _("You have been logged out successfully."))

    return redirect(f"{reverse('accounts:login')}?lang={lang_code}")


def profile_view(request):
    lang_code = set_language(request)

    return render(request, "accounts/profile.html")
    # if request.user.is_authenticated:
    #     social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
    #     if social_account:
    #         messages.info(request, _("Google account is connected."))
    #     else:
    #         messages.warning(request, _("No connected Google account."))
    #     return render(request, "accounts/profile.html")
    # else:
    #     return redirect('accounts:login')


def connect_google_drive(request):
    lang_code = set_language(request)

    if request.user.is_authenticated:
        print(f"Current user ID: {request.user.id}, email: {request.user.email}")
        social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
        print(f"Social Account found: {social_account}")

        if social_account:
            token = SocialToken.objects.filter(account=social_account).first()

            if token:

                if token.expires_at < timezone.now():
                    print("Access token expired. Refreshing the token...")
                    creds = Credentials(
                        token=None,
                        refresh_token=token.token_secret,
                        token_uri='https://oauth2.googleapis.com/token',
                        client_id=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                        client_secret=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                    )
                    creds.refresh(Request())

                    expiry_seconds = (creds.expiry - datetime.now()).total_seconds()
                    token.expires_at = timezone.now() + timedelta(seconds=expiry_seconds)
                    token.save()
                    print("Token refreshed and saved.")

                creds = Credentials(
                    token=token.token,
                    refresh_token=token.token_secret,
                    token_uri='https://oauth2.googleapis.com/token',
                    client_id=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                    client_secret=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                )

                try:
                    service = build('drive', 'v3', credentials=creds)
                    results = service.files().list(pageSize=10, fields="files(id, name, thumbnailLink)").execute()
                    print(f"Google Drive API response: {results}")
                    files = results.get('files', [])
                    return render(request, 'accounts/google_drive.html', {'files': files})

                except Exception as e:
                    print(f"Error while accessing Google Drive API: {e}")
                    messages.error(request, _("Error accessing Google Drive."))
                    return redirect(f"{reverse('accounts:profile')}?lang={lang_code}")

            else:
                messages.error(request, _("Google token not found."))

        else:
            messages.error(request, _("No Google account connected."))

    else:
        messages.error(request, _("You need to log in to connect to Google Drive."))

    return redirect(f"{reverse('accounts:profile')}?lang={lang_code}")


def google_login_callback(request):
    lang_code = set_language(request)

    social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
    if social_account:
        token = SocialToken.objects.filter(account=social_account).first()
        if token:
            print(f"Token exists for user {request.user}: {token.token}")
        else:
            print("Token not found.")
    else:
        print("Social account not found.")

    return redirect(f"{reverse('accounts:profile')}?lang={lang_code}")