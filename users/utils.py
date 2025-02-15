from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(user_email, username):
    subject = 'Welcome to Our Platform!'
    message = f'Hi {username},\n\nThank you for signing up on our platform. We are excited to have you on board!'
    from_email = settings.DEFAULT_FROM_EMAIL

    # Send the email
    send_mail(
        subject,
        message,
        from_email,
        [user_email],
        fail_silently=False,
    )
