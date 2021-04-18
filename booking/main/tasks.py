from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from booking.booking.celery import app
from .models import Room, Subscriber


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
