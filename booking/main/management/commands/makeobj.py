import factory
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory

from main.models import Room, AccommodationFacility, AccommodationManager


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.LazyAttribute(lambda a: "{}_{}@example.com".format(a.last_name.lower(), a.first_name[0].lower()))


class ManagerHotelFactory(DjangoModelFactory):
    class Meta:
        model = AccommodationManager

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    middle_name = ""
    profile = factory.SubFactory(UserFactory)


class Command(BaseCommand):
    help = "Make some object for inti booking project"

    def add_arguments(self, parser) -> None:
        parser.add_argument('hotel_names', nargs="+", type=str)

    def handle(self, *args, **options):
        for name in options["hotel_names"]:
            hotel = AccommodationFacility.objects.create(
                title=name,
                num_stars=5,
                accommodation_type=6,
                address="Заполнить адрес",
                email="info@{}.com".format(name.lower()),
                description="Отель {}".format(name),
                manager=ManagerHotelFactory.create()
            )

            for i in range(4):
                Room.objects.create(
                    hotel=hotel,
                    number="10{}".format(i),
                    description="Номер в {}".format(hotel.title),
                    area=40+i*5
                )
