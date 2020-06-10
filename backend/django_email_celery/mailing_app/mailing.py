from celery import shared_task

from django.core.mail import send_mail

from time import sleep

@shared_task
def sleepy(duration):
    sleep(duration)
    return None

@shared_task
def send_email_task():
    send_mail('Celery Task Worked!',
    'This is proof the task worked!',
    'quechi8933@gmail.com',
    ['celery1234@agilekz.com'])

    return None
