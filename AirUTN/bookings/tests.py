from django.urls import resolve
from django.test import TestCase
from .models import City, Property
from django.contrib.auth.models import User

class CityTests(TestCase):
    def setUp(self):
        City.objects.create(name='Tandil')
    
    def test_city_persistance(self):
        self.assertTrue(City.objects.exists())    
        
class PropertyTopicsTests(TestCase):
    def setUp(self):
        city = City.objects.create(name='La Plata')
        user = User.objects.create_user(username='testuser', password='12345')
        Property.objects.create(name='Casa de Marcos', description='Casa de verano',
        picture=None, max_pax=4, daily_cost=1500, city=city, owner=user)
    
    def test_property_persistance(self):
        self.assertTrue(Property.objects.exists())