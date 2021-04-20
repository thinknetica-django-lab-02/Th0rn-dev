import datetime
import random
from vonage import Client, Sms
from celery.schedules import crontab
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decouple import config

from booking.celery import app
from .models import Room, Subscriber, SMSLog


app.conf.beat_schedule={
    'add-every-week': {
        'task': 'tasks.send_week_news_mail',
        'schedule': crontab(minute=0, hour=10, day_of_week='mon')
    }
}


@app.task(name="send_newsleter")
def send_newsleter():
    room = Room.objects.last()
    subject = 'Создан новый объект размещения в ' + room.hotel
    html_message = render_to_string('main/mail_subscribers.html', {'room': room})
    plain_message = strip_tags(html_message)
    from_email = 'From <from@example.com>'
    to = Subscriber.objects.values_list("receiver__email", flat=True)
    send_mail(
        subject,
        plain_message,
        from_email,
        [to],
        html_message=html_message)


@app.task(name="send_week_news_mail")
def send_week_news():
    today = datetime.date.today()
    week_ago = datetime.timedelta(deys=7)
    diff = today - week_ago
    rooms = Room.objects.filter(created_gte=diff)
    if rooms:
        subject = 'номера, добавленные за последнюю неделю'
        html_message = render_to_string('main/mail_week_news.html', {'rooms': rooms})
        plain_message = strip_tags(html_message)
        from_email = 'from <from@example.com>'
        to = Subscriber.objects.values_list("receiver__email", flat=True)
        send_mail(
            subject,
            plain_message,
            from_email,
            [to],
            html_message=html_message)


@app.task(name="send_sms")
def send_sms_by_vonage():
    key = config("KEY")
    secret = config("SECRET")
    phone = config("PHONE")
    rnd_num = random.randint(1000, 9999)
    client = Client(key=key, secret=secret)
    sms = Sms(client)
    resp = sms.send_message({
        "from": "booking test",
        "to": phone,
        "text": rnd_num
    })
    status = resp["messages"][0]["status"]
    if status == "0":
        SMSLog.objects.create(
            status=status,
            message=rnd_num,
            response="message delivered "
        )
    else:
        SMSLog.objects.create(
            status=status,
            message=rnd_num,
            response=resp['messages'][0]['error-text']
        )
