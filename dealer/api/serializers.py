from rest_framework import serializers
from dealer.models import Store, Car, Transaction


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'budget']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'price', 'store', 'submission_date']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'car_make', 'car_model', 'buyer', 'seller', 'transaction_type', 'transaction_amount', 'transaction_date']
