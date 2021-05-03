import datetime
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from sorl.thumbnail import ImageField
from django.contrib.postgres.fields import ArrayField

from .validators import validate_age


class AccommodationManager(models.Model):
    """
    Model manager of accomodation facility
    """
    first_name = models.CharField("Имя", max_length=30)
    middle_name = models.CharField("Отчествво", max_length=30)
    last_name = models.CharField("Фамилия", max_length=30)
    profile = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Профиль"
    )

    def __str__(self) -> str:
        return "{} {} {}".format(
            self.last_name,
            self.first_name,
            self.middle_name
        )


class AccommodationFacility(models.Model):
    """
    Model accomodation facility: hotels, cempings etc
    """
    RATING_STARS = [
        ("1", "Одна звезда"),
        ("2", "Две звезды"),
        ("3", "Три звезды"),
        ("4", "Четыре звезды"),
        ("5", "Пять звезд")
    ]
    ACCOMMODATION_TYPES = [
        ("1", "Резорт"),
        ("2", "Бутик-отель"),
        ("3", "Апартаменты"),
        ("4", "Апарт-отель"),
        ("5", "Вилла"),
        ("6", "Бизнес-отель"),
        ("7", "Спа-отель"),
        ("8", "Шале"),
        ("9", "Лоджи"),
        ("0", "Кемпинг"),
        ("11", "Мотель"),
        ("12", "Отели типа «постель и завтрак»"),
        ("13", "Хостел"),
    ]
    title = models.CharField("Название", max_length=100)
    num_stars = models.CharField(
        "Рейтинг размещения",
        max_length=1,
        choices=RATING_STARS
    )
    accommodation_type = models.CharField(
        "Тип размещения",
        max_length=2,
        choices=ACCOMMODATION_TYPES
    )
    address = models.CharField("Адрес", max_length=120)
    email = models.EmailField()
    description = models.TextField("Описание", blank=True)
    image = ImageField(upload_to='images/')
    manager = models.ForeignKey(
        AccommodationManager,
        on_delete=models.CASCADE,
        verbose_name="Управляющий"
    )

    def __str__(self) -> str:
        return self.title


class Room(models.Model):
    """
    A model room for accommodation facility.
    """
    STATUS_CHOICES = [
        ('d', 'Draft'),
        ('p', 'Published'),
        ('a', 'Arhived'),
    ]

    hotel = models.ForeignKey(
        AccommodationFacility,
        on_delete=models.CASCADE,
        default="",
        verbose_name="Отель"
    )
    number = models.CharField("Номер комнаты", max_length=10)
    checkin = models.TimeField(
        "Время заезда",
        auto_now=False,
        default=datetime.time(12, 00)
    )
    checkout = models.TimeField(
        "Время выселения",
        auto_now=False,
        auto_now_add=False,
        default=datetime.time(10, 00)
    )
    booking = models.BooleanField("Номер забронирован", default=False)
    description = models.TextField("Описание", blank=True)
    area = models.DecimalField(
        "Площадь комнаты",
        blank=True,
        max_digits=3,
        decimal_places=1
    )
    tags = ArrayField(models.CharField(max_length=30, blank=True), blank=True)
    rental = models.DecimalField(
        verbose_name="Аренда за сутки",
        max_digits=5,
        decimal_places=1,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="Статус", default="Draft")

    def __str__(self) -> str:
        return "{} - номер {}".format(self.hotel.title, self.number)

    def get_absolute_url(self) -> str:
        return reverse('room-detail', kwargs={'id': self.id})


class Profile(models.Model):
    """
    A model Profile extends standarts Django model User, augmenting the
    attributes without changing the User model (avatar, birth day, etc).
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=False
    )
    birthday = models.DateField(
        verbose_name="День рождения",
        validators=[validate_age]
    )
    avatar = ImageField(upload_to='avatar/')

    def __str__(self) -> str:
        return "Профиль пользователя {}".format(self.user.first_name)


class Subscriber(models.Model):
    """
    A model Subscriber for creating a mailing list
    """
    receiver = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.receiver.email


class SMSLog(models.Model):
    """
    A model that implements the logging of messages sent through the external API
    """
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(verbose_name="Статус")
    message = models.CharField(verbose_name="Сообщение", max_length=100)
    response = models.TextField("Ответ")
