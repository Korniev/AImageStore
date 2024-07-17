from datetime import datetime, timedelta

import pyotp
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from .models import User


def send_otp(request, email, purpose='verification'):
    user = User.objects.get(email=email)
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=5)
    request.session['otp_valid_date'] = str(valid_date)

    print(f"Your one time password if {otp} is valid until {valid_date}")

    # відправка на пошту
    subject = "Confirm email for AImageStore"
    html_message = render_to_string('accounts/email_template.html', {'user_username': user.username,
                                                                     'otp_code': otp, 'purpose': purpose})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]

    mail = EmailMultiAlternatives(subject, plain_message, from_email, to_email)
    mail.attach_alternative(html_message, "text/html")
    mail.send()
