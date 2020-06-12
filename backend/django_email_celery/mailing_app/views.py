from django.shortcuts import render
from django.http import HttpResponse

from .tasks import send_email_task

def index(request):
    # send_email_task.delay()
    send_email_task.delay()
    return HttpResponse('<h1>EMAIL HAS BEEN SENT OMG!</h1>')