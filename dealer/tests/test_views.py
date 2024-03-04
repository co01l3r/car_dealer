from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.test import RequestFactory

from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage

from dealer.views import submit_car, buy_car, car_list, transactions_summary
from dealer.models import Store, Car, Transaction


class SubmitCarViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_submit_car_post(self):
        store = Store.objects.create(name='Test Store', budget=10000)
        url = reverse('submit_car')
        data = {
            'make': 'Test Make',
            'model': 'Test Model',
            'price': 1000
        }
        request = self.factory.post(url, data)
        response = submit_car(request)
        self.assertEqual(response.status_code, 302)

        # Check if the car object is created
        car_exists = Car.objects.filter(make='Test Make', model='Test Model').exists()
        self.assertTrue(car_exists)

        # Check if the store budget is updated
        updated_store = Store.objects.get(id=store.id)
        self.assertEqual(updated_store.budget, 9000)


class BuyCarViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.store = Store.objects.create(name='Test Store', budget=Decimal('25000.00'))
        self.car = Car.objects.create(make='Test Make', model='Test Model', price=Decimal('5000.00'), store=self.store)

    def test_buy_car(self):
        request_factory = RequestFactory()
        request = request_factory.post(reverse('buy_car', kwargs={'car_id': self.car.id}))
        request.user = self.user

        # Set up messages
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = buy_car(request, self.car.id)
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Car.objects.filter(id=self.car.id).exists())
        self.assertTrue(Transaction.objects.filter(car_make='Test Make', car_model='Test Model').exists())


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.store = Store.objects.create(name='Test Store', budget=25000)
        Car.objects.create(make='Make1', model='Model1', price=5000, store=self.store)
        Car.objects.create(make='Make2', model='Model2', price=7500, store=self.store)
        Car.objects.create(make='Make3', model='Model3', price=6000, store=self.store)

    def test_car_list_view(self):
        # Create a mock request
        request = RequestFactory().get('/car-list/?ordering=-price')
        request.user = self.user

        # Call the view function
        response = car_list(request)
        self.assertEqual(response.status_code, 200)


class TransactionsSummaryViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Create some test transactions
        Transaction.objects.create(transaction_type='bought', transaction_amount=5000)
        Transaction.objects.create(transaction_type='bought', transaction_amount=7500)
        Transaction.objects.create(transaction_type='sold', transaction_amount=6000)
        Transaction.objects.create(transaction_type='sold', transaction_amount=3000)

    def test_transactions_summary_view(self):
        # Create a mock request
        request = RequestFactory().get('/transactions-summary/')
        request.user = self.user

        # Call the view function
        response = transactions_summary(request)
        self.assertEqual(response.status_code, 200)

        # Check the calculated summary values directly
        total_bought_amount = Transaction.total_bought_amount()
        total_sold_amount = Transaction.total_sold_amount()
        total_transaction_count = Transaction.total_transaction_count()
        total_bought_transaction_count = Transaction.total_bought_transaction_count()
        total_sold_transaction_count = Transaction.total_sold_transaction_count()

        # Assert the correctness of the calculated summary values
        self.assertEqual(total_bought_amount, 12500)
        self.assertEqual(total_sold_amount, 9000)
        self.assertEqual(total_transaction_count, 4)
        self.assertEqual(total_bought_transaction_count, 2)
        self.assertEqual(total_sold_transaction_count, 2)

