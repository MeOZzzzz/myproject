import zoneinfo
from datetime import timezone

from django.test import TestCase
from shop.models import *

class TestDataBase(TestCase):
    fixtures = [
        "shop/fixtures/data.json"
    ]

    def setUp(self):
        self.user = User.objects.get(username='root')

    def test_user_exists(self):
        users = User.objects.all()
        users_number = users.count()
        user = users.first()
        self.assertEqual(users_number, 1)
        self.assertEqual(user.username, 'root')
        self.assertTrue(user.is_superuser)

    def test_user_check_password(self):
        self.assertTrue(self.user.check_password('B@ttelf1lde'))

    def find_cart_number(self):
        cart_number = Order.objects.filter(user=self.user,
                                           status=Order.STATUS_CART
                                           ).count()
        return cart_number
    def test_function_get_cart(self):

        self.assertEqual(self.find_cart_number(),0)
        Order.get_card(self.user)

        self.assertEqual(self.find_cart_number(), 1)
        Order.get_card(self.user)

        self.assertEqual(self.find_cart_number(), 1)

    def test_cart_older_7days(self):
        cart = Order.get_card(self.user)
        cart.creation_time = timezone.datetime(2000,1,1,tzinfo=zoneinfo.ZoneInfo('UTC'))
        cart.save()
        cart = Order.get_card(self.user)
        self.assertEqual((timezone.now()-cart.creation_time).days,0)