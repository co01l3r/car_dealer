import logging
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dealer.models import Car, Store, Transaction
from .serializers import StoreSerializer, CarSerializer, TransactionSerializer


@api_view(['GET'])
def get_routes(request):
    """
    Get a list of available API endpoints.

    Returns:
        Response: A JSON response containing a list of available API endpoints.
    """
    routes = [
        '/api/stores',
        '/api/stores/<int:pk>',

        '/api/cars',
        '/api/car_list/?ordering=ORDERING_OPTION>',
        '/api/cars/submit',
        '/api/cars/<int:pk>/buy',

        '/api/transactions/',
        '/api/transactions/summary',
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
def store_list_create_api_view(request: Request) -> Response:
    """
    API view for listing and creating stores.

    Args:
        request (Request): The HTTP request object.

    Returns:
        Response: The HTTP response containing store data or validation errors.

    Raises:
        None
    """
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


@api_view(['GET'])
def get_store_with_cars(request: Request, pk: int) -> Response:
    """
    API view for retrieving a store along with its associated cars.

    Args:
        request (Request): The HTTP request object.
        pk (int): The primary key of the store to retrieve.

    Returns:
        Response: The HTTP response containing store and cars data.

    Raises:
        HTTP 404 Error: If the requested store does not exist.
        HTTP 500 Error: If an unexpected error occurs while fetching store information.
    """
    try:
        store = get_object_or_404(Store, pk=pk)
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


@api_view(['POST'])
def submit_car_for_purchase(request: Request) -> Response:
    """
    API view for submitting a car for purchase.

    Args:
        request (Request): The HTTP request object containing car data.

    Returns:
        Response: The HTTP response indicating the success or failure of the car submission.

    Raises:
        HTTP 400 Error: If the request data is invalid.
        HTTP 400 Error: If the store does not have enough budget to buy the car.
        HTTP 500 Error: If an unexpected error occurs during the car submission process.
    """
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
def purchase_car(request: Request, car_id: int) -> Response:
    """
    API view for purchasing a car.

    Args:
        request (Request): The HTTP request object.
        car_id (int): The ID of the car to be purchased.

    Returns:
        Response: The HTTP response indicating the success or failure of the car purchase.

    Raises:
        HTTP 500 Error: If an unexpected error occurs during the car purchase process.
    """
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
def car_list(request: Request) -> Response:
    """
    API view for listing cars.

    Args:
        request (Request): The HTTP request object.

    Returns:
        Response: The HTTP response containing the list of cars.

    Raises:
        HTTP 500 Error: If an unexpected error occurs while fetching the list of cars.
    """
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
def transactions_summary(request: Request) -> Response:
    """
    API view for summarizing transactions.

    Args:
        request (Request): The HTTP request object.

    Returns:
        Response: The HTTP response containing the summary of transactions.

    Raises:
        HTTP 500 Error: If an unexpected error occurs while summarizing transactions.
    """
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
def transaction_list(request: Request) -> Response:
    """
    API view for listing transactions.

    Args:
        request (Request): The HTTP request object.

    Returns:
        Response: The HTTP response containing the list of transactions.

    Raises:
        HTTP 500 Error: If an unexpected error occurs while fetching the transactions.
    """
    try:
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    except Exception as e:
        logging.error(f"An error occurred in transaction_list view: {e}")
        return Response({'error': 'An unexpected error occurred. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
