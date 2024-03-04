import logging
from dealer.models import Store
from .serializers import StoreSerializer, CarSerializer, TransactionSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dealer.models import Car, Store, Transaction
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Q


@api_view(['GET', 'POST'])
def store_list_create_api_view(request):
    if request.method == 'GET':
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def submit_car(request):
    serializer = CarSerializer(data=request.data)
    if serializer.is_valid():
        car = serializer.save()

        store = get_object_or_404(Store)

        if store.budget >= car.price:
            try:
                with transaction.atomic():
                    car.store = store
                    car.save()
                    store.budget -= car.price
                    store.save()

                    # Create transaction object
                    Transaction.objects.create(
                        car_make=car.make,
                        car_model=car.model,
                        buyer=store.name,
                        seller='User',
                        transaction_type='bought',
                        transaction_amount=car.price
                    )

                    return Response(status=status.HTTP_302_FOUND)
            except Exception as e:
                logging.error(f"An error occurred while submitting car: {e}")
                return Response({'error': 'An unexpected error occurred. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'warning': 'The store does not have enough money to buy this car.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def buy_car(request, car_id):
    try:
        with transaction.atomic():
            car = get_object_or_404(Car, id=car_id)
            store = car.store
            transaction_amount = car.price

            # Create transaction object
            transaction_obj = Transaction.objects.create(
                car_make=car.make,
                car_model=car.model,
                buyer='User',
                seller=store.name,
                transaction_type='sold',
                transaction_amount=transaction_amount
            )

            if transaction_obj:
                store.budget += transaction_amount
                store.save()

                car.delete()

                return Response({'message': 'Car successfully purchased.'}, status=status.HTTP_200_OK)

    except Exception as e:
        logging.error(f"An error occurred while buying car: {e}")

    return Response({'error': 'An unexpected error occurred. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def store_info(request):
    try:
        store = get_object_or_404(Store)
        cars = Car.objects.filter(store=store)

        store_serializer = StoreSerializer(store)
        cars_serializer = CarSerializer(cars, many=True)

        data = {
            'store': store_serializer.data,
            'cars': cars_serializer.data
        }

        return Response(data)
    except Exception as e:
        logging.error(f"An error occurred while fetching store information: {e}")
        return Response({'error': 'An unexpected error occurred while fetching store information.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def car_list(request):
    try:
        ordering_options = {
            'price': 'price',
            '-price': '-price',
            'make': 'make',
            '-make': '-make',
            'model': 'model',
            '-model': '-model',
            'submission_date': 'submission_date',
            '-submission_date': '-submission_date',
        }

        # Get the user's selected ordering option, defaulting to 'price' if not provided or invalid
        ordering = request.GET.get('ordering', 'price')
        ordering_field = ordering_options.get(ordering, 'price')

        cars = Car.objects.all().order_by(ordering_field)

        serializer = CarSerializer(cars, many=True)

        return Response(serializer.data)
    except Exception as e:
        logging.error(f"An error occurred in car_list view: {e}")
        return Response({'error': 'An unexpected error occurred. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def transactions_summary(request):
    try:
        total_bought_amount = Transaction.total_bought_amount()
        total_sold_amount = Transaction.total_sold_amount()
        total_transaction_count = Transaction.total_transaction_count()
        total_bought_transaction_count = Transaction.total_bought_transaction_count()
        total_sold_transaction_count = Transaction.total_sold_transaction_count()

        data = {
            'total_bought_amount': total_bought_amount,
            'total_sold_amount': total_sold_amount,
            'total_transaction_count': total_transaction_count,
            'total_bought_transaction_count': total_bought_transaction_count,
            'total_sold_transaction_count': total_sold_transaction_count,
        }

        return Response(data)
    except Exception as e:
        logging.error(f"An error occurred in transactions_summary view: {e}")
        return Response({'error': 'An unexpected error occurred. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def transaction_list(request):
    try:
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.error(f"An error occurred in transaction_list view: {e}")
        return Response({'error': 'An unexpected error occurred. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)