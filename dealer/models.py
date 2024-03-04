import logging

from django.db import models


# store
class Store(models.Model):
    name = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.name


# car
class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='cars')
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.make} - {self.model}"


# transaction
class Transaction(models.Model):
    TRANSACTION_TYPES: tuple = (
        ('bought', 'Bought'),
        ('sold', 'Sold'),
    )

    car_make = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    buyer = models.CharField(max_length=100)
    seller = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def total_bought_amount(cls) -> float:
        try:
            total = cls.objects.filter(transaction_type='bought').aggregate(total=models.Sum('transaction_amount'))['total']
            return total or 0
        except Exception as e:
            logging.error(f"Error occurred while calculating total bought amount: {e}")
            return 0

    @classmethod
    def total_sold_amount(cls) -> float:
        try:
            total = cls.objects.filter(transaction_type='sold').aggregate(total=models.Sum('transaction_amount'))['total']
            return total or 0
        except Exception as e:
            logging.error(f"Error occurred while calculating total sold amount: {e}")
            return 0

    @classmethod
    def total_transaction_count(cls) -> int:
        try:
            return cls.objects.count()
        except Exception as e:
            logging.error(f"Error occurred while calculating total transaction count: {e}")
            return 0

    @classmethod
    def total_bought_transaction_count(cls) -> int:
        try:
            return cls.objects.filter(transaction_type='bought').count()
        except Exception as e:
            logging.error(f"Error occurred while calculating total bought transaction count: {e}")
            return 0

    @classmethod
    def total_sold_transaction_count(cls) -> int:
        try:
            return cls.objects.filter(transaction_type='sold').count()
        except Exception as e:
            logging.error(f"Error occurred while calculating total sold transaction count: {e}")
            return 0

    def __str__(self) -> str:
        return f"{self.transaction_type} - {self.transaction_amount} - {self.transaction_date}"
