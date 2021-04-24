from django.contrib.auth.models import User
from .main.models import Tag, Room, AccommodationFacility, AccommodationManager

user1 = User.objects.create(
    username="manager1",
    email="m1@example.com",
    password="test1"
)

user2 = User.objects.create(
    username="manager2",
    email="m2@example.com",
    password="test2"
)

m1 = AccommodationManager.objects.create(
    first_name="Константин",
    middle_name="Иванович",
    last_name="Петров",
    profile=user1
)

m2 = AccommodationManager.objects.create(
    first_name="Алексей",
    middle_name="Петрович",
    last_name="Сидоров",
    profile=user2
)

t1 = Tag(tag_name="завтрак в номер")
t1.save()

t2 = Tag(tag_name="трансфер до аэропорта")
t2.save()

t3 = Tag(tag_name="бесплатный wifi")
t3.save()

f1 = AccommodationFacility(
    title="Hilton",
    num_starts=5,
    accommodation_type=6,
    address="Москва, ул. Тихая",
    email="info@hilton.com",
    description="Отель Хилтон",
    manager=m1
)
f1.save()

f2 = AccommodationFacility(
    title="Redison",
    num_starts=5,
    accommodation_type=6,
    address="Москва, ул. Громкая",
    email="info@redison.com",
    description="Отель Редисон",
    manager=m1
)
f2.save()

r1 = Room(
    hotel=f1,
    number="102",
    description="Номер в Хилтон",
    area=40.5
)
r1.save()
r1.tag.add(t1, t2)

r2 = Room(
    hotel=f1,
    number="301",
    description="Номер в Хилтон",
    area=40.5
)
r2.save()
r2.tag.add(t3)

r3 = Room(
    hotel=f2,
    number="101",
    description="Номер в Редисон",
    area=30.0
)
r3.save()
r3.tag.add(t3)

r4 = Room(
    hotel=f2,
    number="201",
    description="Номер в Редисон",
    area=50.0
)
r4.save()

r5 = Room(
    hotel=f2,
    number="301",
    description="Номер в Редисон",
    area=50.0
)
r5.save()

r5.tag.add(t1)

Room.objects.all()
AccommodationFacility.objects.all()

Room.objects.filter(hotel=f1)
Room.objects.filter(hotel=f2).exclude(area__gte=40.0)
