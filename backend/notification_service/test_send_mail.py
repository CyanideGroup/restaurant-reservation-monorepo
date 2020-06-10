from django.conf import settings
from django.core.mail import send_mail
from django.template import Engine, Context

from django_email_celery.django_email_celery.celery import app
from django_email_celery.mailing_app.mailing import send_email_task

def render_template(template, context):
    engine = Engine.get_default()

    tmpl = engine.get_template(template)

    return tmpl.render(Context(context))


@app.task
def try_mail_task(recipients='', subject='', template='', context=''):
    send_email_task()

try_mail_task()
print("Opps")