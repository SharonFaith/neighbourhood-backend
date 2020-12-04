import os

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .token import activation_token


def send_activation_email(request, user):
    message = Mail(
        from_email="moringacoreprojects@gmail.com",
        to_emails=user.email,
        subject="Account Activation",
        html_content=render_to_string('emails/activation_email.html', {
            'user': user,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': activation_token.make_token(user)
        }))

    try:
        sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print("SENDGRID RESPONSE: ", response.status_code)
    except Exception as e:
        print("\nSENDGRID ERROR: ", e, "\n")
