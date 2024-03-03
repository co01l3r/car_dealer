from django.db import models


# store
class Store(models.Model):
    name = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)


# car
class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='cars')


# transaction
class Transaction(models.Model):
    car_make = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    buyer = models.CharField(max_length=100)
    seller = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=10)  # 'buy' or 'sell'
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
