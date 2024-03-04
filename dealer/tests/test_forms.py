from django.test import TestCase
from dealer.forms import CarForm


class CarFormTest(TestCase):
    def test_car_form_valid_data(self):
        form = CarForm(data={
            'make': 'Toyota',
            'model': 'Camry',
            'price': 25,
        })
        self.assertTrue(form.is_valid())

    def test_car_form_invalid_data(self):
        form = CarForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)
        