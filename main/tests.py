from django.test import TestCase
from .models import Hood
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.
class TestHood(TestCase):
    """
    """
    def setUp(self):
        self.hood = Hood.objects.create(name='Hood 1', local_area="Kilimani", city_town='Nairobi', country='Kenya')
        self.user = User.objects.create(first_name='John', last_name='Doe', email='johndoe@example.com', username='john_doe', password='password')

    def tearDown(self):
        pass

    def test_instance(self):
        """
        Test if instance of Hood
        """
        self.assertIsInstance(self.hood, Hood)

    def test_attributes(self):
        """
        Test if attributes are createed correctly
        """
        pass
    def test_occupants(self):
        self.user.hood = self.hood
        self.user.save()
        no_of_users = self.hood.occupants
        self.assertTrue(no_of_users > 0)

