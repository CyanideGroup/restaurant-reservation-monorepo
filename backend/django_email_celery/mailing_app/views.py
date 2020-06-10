from django.shortcuts import render
from django.http import HttpResponse

from .mailing import sleepy, send_email_task

def index(request):
    # send_email_task.delay()
    send_email_task()
    return HttpResponse('<h1>EMAIL HAS BEEN SENT OMG!</h1>')