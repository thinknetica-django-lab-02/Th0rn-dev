import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Room, Subscriber


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
        to = [subscriber.receiver.email for subscriber in Subscriber.objects.all()]
        send_mail(
            subject,
            plain_message,
            from_email,
            [to],
            html_message=html_message)


# scheduler = BackgroundScheduler()
# scheduler.add_job(send_week_news, 'cron', week="*")
# scheduler.start()
