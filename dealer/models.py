from django.db import models


# store
class Store(models.Model):
    name = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


# car
class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='cars')
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.make} - {self.model}"


# transaction
class Transaction(models.Model):
    TRANSACTION_TYPES = (
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
    def total_bought_amount(cls):
        return cls.objects.filter(transaction_type='bought').aggregate(total=models.Sum('transaction_amount'))['total'] or 0

    @classmethod
    def total_sold_amount(cls):
        return cls.objects.filter(transaction_type='sold').aggregate(total=models.Sum('transaction_amount'))['total'] or 0

    @classmethod
    def total_transaction_count(cls):
        return cls.objects.count()

    @classmethod
    def total_bought_transaction_count(cls):
        return cls.objects.filter(transaction_type='bought').count()

    @classmethod
    def total_sold_transaction_count(cls):
        return cls.objects.filter(transaction_type='sold').count()

    def __str__(self):
        return f"{self.transaction_type} - {self.transaction_amount} - {self.transaction_date}"
