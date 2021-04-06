import datetime
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User


class AccommodationManager(models.Model):
    first_name = models.CharField("Имя", max_length=30)
    middle_name = models.CharField("Отчествво", max_length=30)
    last_name = models.CharField("Фамилия", max_length=30)
    profile = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name="Профиль")

    def __str__(self):
        return self.last_name + " " + self.first_name + " " + self.middle_name


class AccommodationFacility(models.Model):
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
    num_starts = models.CharField("Рейтинг размещения", max_length=1, choices=RATING_STARS)
    accommodation_type = models.CharField("Тип размещения", max_length=2, choices=ACCOMMODATION_TYPES)
    address = models.CharField("Адрес", max_length=120)
    email = models.EmailField()
    description = models.TextField("Описание", blank=True)
    image = models.ImageField(upload_to="images", blank=True)
    manager = models.ForeignKey(AccommodationManager, on_delete=models.CASCADE, verbose_name="Управляющий")

    def __str__(self):
        return self.title


class Tag(models.Model):
    tag_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.tag_name


class Room(models.Model):
    hotel = models.ForeignKey(AccommodationFacility, on_delete=models.CASCADE, default="", verbose_name="Отель")
    number = models.CharField("Номер комнаты", max_length=10)
    checkin = models.TimeField("Время заезда", auto_now=False, default=datetime.time(12, 00))
    checkout = models.TimeField("Время выселения", auto_now=False, auto_now_add=False, default=datetime.time(10, 00))
    booking = models.BooleanField("Номер забронирован", default=False)
    description = models.TextField("Описание", blank=True)
    area = models.DecimalField("Площадь комнаты", blank=True, max_digits=3, decimal_places=1)
    image = models.ImageField(blank=True)
    tags = models.ManyToManyField(Tag, verbose_name="Теги", blank=True)
    rental = models.DecimalField(verbose_name="Аренда за сутки", max_digits=5, decimal_places=1, null=True)

    def __str__(self):
        return "{} - номер {}".format(self.hotel.title, self.number)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=False)

    def __str__(self):
        return "Профиль пользователя {}".format(self.user.first_name)


# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = "__all__"

