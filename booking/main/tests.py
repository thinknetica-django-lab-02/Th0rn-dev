from django.test import TestCase, Client
from django.contrib.auth.models import User
from unittest import skip

from .models import Room, AccommodationManager, AccommodationFacility

client = Client()


class TestViews(TestCase):

    def setUp(self):
        # создать отель, менегера, комнату
        user = User.objects.create(
            username="manager",
            email="m1@example.com",
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

    def test_index(self):
        """Test main page view"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_rooms_list(self):
        """Test room list page view"""
        response = self.client.get('/rooms/')
        self.assertEqual(response.status_code, 200)

    def test_room_detail(self):
        """Test room detail page view for saved room"""
        room = Room.objects.first()
        response = self.client.get("/rooms/{}/".format(room.id))
        self.assertEqual(response.status_code, 200)

    # @skip('skip test room create')
    def test_room_create(self):
        """Test room create view"""
        resp = client.post(
            "/accounts/login/?next=/room/add/",
            {
                "username": "manager",
                "password": "test"
            })
        self.assertEqual(resp.status_code, 200)

    # @skip('skip test room edit')
    def test_room_edit(self):
        """Test room edit view, require authorization"""
        room = Room.objects.first()
        resp = client.post(
            "/accounts/login/?next=/rooms/{}/edit/".format(room.id),
            {
                "username": "manager",
                "password": "test"
            })
        self.assertEqual(resp.status_code, 200)

    def test_profile(self):
        """Test accounts profile view"""
        resp = client.post(
            "/accounts/login/?next=/accounts/profile/",
            {
                "username": "manager",
                "password": "test"
            })
        self.assertEqual(resp.status_code, 200)

    @skip('void tets dont delete skip')
    def test_void(self):
        """Dont delete skip decorator"""
        pass
