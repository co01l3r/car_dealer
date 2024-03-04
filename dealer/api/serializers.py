from rest_framework import serializers

from dealer.models import Store, Car, Transaction


class StoreSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Store model.

    Serializes Store model instances into JSON representations and vice versa.

    Attributes:
        model (Model): The model class that the serializer should serialize/deserialize.
        fields (list): The fields of the model that should be included in the serialized representation.
    """
    class Meta:
        model = Store
        fields = ['id', 'name', 'budget']


class CarSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Car model.

    Serializes Car model instances into JSON representations and vice versa.

    Attributes:
        model (Model): The model class that the serializer should serialize/deserialize.
        fields (list): The fields of the model that should be included in the serialized representation.
    """
    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'price', 'store', 'submission_date']


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Transaction model.

    Serializes Transaction model instances into JSON representations and vice versa.

    Attributes:
        model (Model): The model class that the serializer should serialize/deserialize.
        fields (list): The fields of the model that should be included in the serialized representation.
    """
    class Meta:
        model = Transaction
        fields = ['id', 'car_make', 'car_model', 'buyer', 'seller', 'transaction_type', 'transaction_amount', 'transaction_date']
