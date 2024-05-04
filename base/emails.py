import imp
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from celery import shared_task
from time import sleep

@shared_task
def send_account_activation_email(email , email_token):
    subject = 'Your account needs to be verified'
    email_from = settings.EMAIL_HOST_USER   
    # message = f'Hi, click on the link to activate your account http://127.0.0.1:8000/accounts/activate/{email_token}'
    message = f'Hi, click on the link to activate your account https://mrunalbooks.com/accounts/activate/{email_token}'
    send_mail(subject , message , email_from , [email])


@shared_task
def send_order_placed_thankyou_email(email):
    subject = "Thank You for placing Order"
    html_message = render_to_string('email/order_placed_thankyou.html')
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject = subject,
        body = plain_message,
        from_email = settings.EMAIL_HOST_USER,
        to = [email]
    )
    message.attach_alternative(html_message, 'text/html')
    message.send()


@shared_task
def send_order_dispatched_email(email):
    subject = "Your Order is Dispatched"
    html_message = render_to_string('email/order_dispatched.html')
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject = subject,
        body = plain_message,
        from_email = settings.EMAIL_HOST_USER,
        to = [email]
    )
    message.attach_alternative(html_message, 'text/html')
    message.send()
    
    
@shared_task
def send_order_shipped_email(email):
    subject = "Your Order is Shipped"
    html_message = render_to_string('email/order_shipped.html')
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject = subject,
        body = plain_message,
        from_email = settings.EMAIL_HOST_USER,
        to = [email]
    )
    message.attach_alternative(html_message, 'text/html')
    message.send()

@shared_task
def send_forget_password_email(email, token):
    subject = 'Your forgot password link'
    # message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/accounts/reset-password/{token}'
    message = f'Hi , click on the link to reset your password https://mrunalbooks.com/accounts/reset-password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


@shared_task
def send_contact_email(name, email, phone, subject, message):
    heading = 'Contact Email from '  + name + " : " + subject 
    email_from = settings.EMAIL_HOST_USER
    message = message + "\nphone no : " + phone + "\nEmail: " + email + "\nName: " + name
    send_mail(heading , message , email_from , [email_from])
    return 0
   