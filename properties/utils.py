# utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_interest_email(user_email, plot_number):
    subject = f"Interest in Plot Number {plot_number}"
    message = f"You have shown interest in Plot Number {plot_number}. A representative will contact you soon."
    from_email = settings.DEFAULT_FROM_EMAIL
    
    send_mail(subject, message, from_email, [user_email])
