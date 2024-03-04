from django.test import TestCase
from dealer.models import Store, Car, Transaction
from datetime import datetime


# store
class StoreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Store.objects.create(name='Test Store', budget=10000.00)

    def test_store_name(self):
        store = Store.objects.get(name='Test Store')
        expected_name = store.name
        self.assertEquals(expected_name, 'Test Store')

    def test_store_budget(self):
        store = Store.objects.get(name='Test Store')
        expected_budget = store.budget
        self.assertEquals(expected_budget, 10000.00)


# car
class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        store = Store.objects.create(name='Test Store', budget=10000.00)
        Car.objects.create(make='Test Make', model='Test Model', price=5000.00, store=store, submission_date=datetime.now())

    def test_car_make(self):
        car = Car.objects.get(id=1)
        expected_make = car.make
        self.assertEquals(expected_make, 'Test Make')

    def test_car_model(self):
        car = Car.objects.get(id=1)
        expected_model = car.model
        self.assertEquals(expected_model, 'Test Model')

    def test_car_price(self):
        car = Car.objects.get(id=1)
        expected_price = car.price
        self.assertEquals(expected_price, 5000.00)

    def test_car_store(self):
        car = Car.objects.get(id=1)
        expected_store = car.store
        self.assertEquals(expected_store.name, 'Test Store')

    def test_car_submission_date(self):
        car = Car.objects.get(id=1)
        expected_submission_date = car.submission_date
        self.assertIsNotNone(expected_submission_date)


# transaction
class TransactionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Transaction.objects.create(
            car_make='Test Make',
            car_model='Test Model',
            buyer='Test Buyer',
            seller='Test Seller',
            transaction_type='bought',
            transaction_amount=1000.00,
        )

    def test_transaction_str(self):
        transaction = Transaction.objects.get(car_make='Test Make')
        expected_str = str(transaction)
        expected_start = 'bought - 1000.00 - '
        self.assertTrue(expected_str.startswith(expected_start))

    def test_total_bought_amount(self):
        total_bought_amount = Transaction.total_bought_amount()
        self.assertEqual(total_bought_amount, 1000.00)

    def test_total_sold_amount(self):
        total_sold_amount = Transaction.total_sold_amount()
        self.assertEqual(total_sold_amount, 0)

    def test_total_transaction_count(self):
        total_transaction_count = Transaction.total_transaction_count()
        self.assertEqual(total_transaction_count, 1)

    def test_total_bought_transaction_count(self):
        total_bought_transaction_count = Transaction.total_bought_transaction_count()
        self.assertEqual(total_bought_transaction_count, 1)

    def test_total_sold_transaction_count(self):
        total_sold_transaction_count = Transaction.total_sold_transaction_count()
        self.assertEqual(total_sold_transaction_count, 0)
