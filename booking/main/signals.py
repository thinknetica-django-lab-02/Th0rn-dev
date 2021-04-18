from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User, Group


from .models import Room, Subscriber


@receiver(post_save, sender=User)
def add_new_user_to_default_group(sender, instance, created, **kwargs):
    if created:
        common_group = Group.objects.get_or_create(name="common users")
        instance.groups.add(common_group[0])
        subject = 'Регистрация нового пользователя на сайте booking'
        html_message = render_to_string('main/mail_new_user.html', {'username': User.username})
        plain_message = strip_tags(html_message)
        from_email = 'From <from@example.com>'
        to = User.email
        send_mail(
            subject,
            plain_message,
            from_email,
            [to],
            html_message=html_message)


@receiver(post_save, sender=Room)
def send_newsleter(sender, instance, created, **kwargs):
    if created:
        subject = 'Создан новый объект размещения в ' + instance.hotel.title
        html_message = render_to_string('main/mail_subscribers.html', {'room': instance})
        plain_message = strip_tags(html_message)
        from_email = 'From <from@example.com>'
        to = Subscriber.objects.values_list("receiver__email", flat=True)
        send_mail(
            subject,
            plain_message,
            from_email,
            [to],
            html_message=html_message)
