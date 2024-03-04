import logging

from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CarForm
from .models import Store, Car, Transaction


def submit_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            store = Store.objects.first()  # Assuming there's only one store for simplicity

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

                        return redirect('store_info')
                except Exception as e:
                    logging.error(f"An error occurred while submitting car: {e}")
                    messages.error(request, 'An unexpected error occurred. Please try again later.')
            else:
                messages.warning(request, 'The store does not have enough money to buy this car.')
    else:
        form = CarForm()

    return render(request, 'dealer/submit_car_form.html', {'form': form})


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

                messages.success(request, 'Car successfully purchased.')
                return redirect('store_info')

    except Exception as e:
        logging.error(f"An error occurred while buying car: {e}")
        messages.error(request, 'An unexpected error occurred. Please try again later.')

    return redirect('store_info')


def store_info(request):
    try:
        store = Store.objects.first()  # Assuming there's only one store for simplicity
        cars = Car.objects.filter(store=store)
        return render(request, 'dealer/store_info.html', {'store': store, 'cars': cars})
    except Exception as e:
        logging.error(f"An error occurred while fetching store information: {e}")
        messages.error(request, 'An unexpected error occurred while fetching store information.')
        return redirect('store_info')


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

        context = {
            'cars': cars,
            'ordering': ordering,
        }
        return render(request, 'dealer/store_info.html', context)
    except Exception as e:
        logging.error(f"An error occurred in car_list view: {e}")
        messages.error(request, 'An unexpected error occurred. Please try again later.')
        return redirect('store_info')


def transactions_summary(request):
    try:
        total_bought_amount = Transaction.total_bought_amount()
        total_sold_amount = Transaction.total_sold_amount()
        total_transaction_count = Transaction.total_transaction_count()
        total_bought_transaction_count = Transaction.total_bought_transaction_count()
        total_sold_transaction_count = Transaction.total_sold_transaction_count()

        context = {
            'total_bought_amount': total_bought_amount,
            'total_sold_amount': total_sold_amount,
            'total_transaction_count': total_transaction_count,
            'total_bought_transaction_count': total_bought_transaction_count,
            'total_sold_transaction_count': total_sold_transaction_count,
        }
        return render(request, 'dealer/transactions.html', context)
    except Exception as e:
        logging.error(f"An error occurred in transactions_summary view: {e}")
        messages.error(request, 'An unexpected error occurred. Please try again later.')
        return redirect('store_info')
