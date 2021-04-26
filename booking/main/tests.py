from django.urls import reverse_lazy
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, Permission
from unittest import skip

from .models import Room, AccommodationManager, AccommodationFacility


class TestViews(TestCase):

    def setUp(self):
        # создать отель, менегера, комнату
        user = User.objects.create_user(
            username="manager",
            email="manager@example.com",
            password="test"
        )
        manager = AccommodationManager.objects.create(
            first_name="Константин",
            middle_name="Иванович",
            last_name="Петров",
            profile=user
        )
        hotel = AccommodationFacility.objects.create(
            title="Hilton",
            num_starts=5,
            accommodation_type=6,
            address="Москва, ул. Тихая",
            email="info@hilton.com",
            description="Отель Хилтон",
            manager=manager
        )
        Room.objects.create(
            hotel=hotel,
            number="101",
            description="Номер в Хилтон",
            area=40.5,
            rental=1200
        )

        editors_grp, _ = Group.objects.get_or_create(name="editors")
        change_room = Permission.objects.get(name="Can change room")
        create_room = Permission.objects.get(name="Can add room")
        editors_grp.permissions.add(change_room)
        editors_grp.permissions.add(create_room)
        editors_grp.user_set.add(user)

        self.client = Client()
        self.client.login(
            username="manager",
            password="test"
        )

    def test_index(self):
        """Test main page view"""
        url = reverse_lazy("index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_rooms_list(self):
        """Test room list page view"""
        url = reverse_lazy("rooms-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_room_detail(self):
        """Test room detail page view for saved room"""
        room = Room.objects.first()
        url = reverse_lazy("room-detail", kwargs={"pk": room.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # @skip('skip test room create')
    def test_room_create(self):
        """Test room create view"""
        url = reverse_lazy("room-add")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # @skip('skip test room edit')
    def test_room_edit(self):
        """Test room edit view, require authorization"""
        room = Room.objects.first()
        url = reverse_lazy("room-edit", kwargs={"pk": room.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_profile(self):
        """Test accounts profile view"""
        url = reverse_lazy("profile")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    @skip('void tets dont delete skip')
    def test_void(self):
        """Dont delete skip decorator"""
        pass
