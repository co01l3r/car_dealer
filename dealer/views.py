from django.shortcuts import render, redirect
from .forms import CarForm
from .models import Store, Car, Transaction


def submit_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            store = Store.objects.first()  # Assuming there's only one store for simplicity
            if store.budget >= car.price:
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
            else:
                return render(request, 'error.html', {'message': 'Store does not have enough budget to buy this car.'})
    else:
        form = CarForm()

    return render(request, 'dealer/submit_car_form.html', {'form': form})


def buy_car(request, car_id):
    car = Car.objects.get(id=car_id)
    store = car.store
    transaction_amount = car.price

    # Create transaction object
    transaction = Transaction.objects.create(
        car_make=car.make,
        car_model=car.model,
        buyer='User',
        seller=store.name,
        transaction_type='sold',
        transaction_amount=transaction_amount
    )

    # Check if the transaction object was created successfully
    if transaction:
        store.budget += transaction_amount
        store.save()

        car.delete()

        return redirect('store_info')
    else:
        return render(request, 'error.html', {'message': 'Failed to create transaction object.'})


def store_info(request):
    store = Store.objects.first()  # Assuming there's only one store for simplicity
    cars = Car.objects.filter(store=store)
    return render(request, 'dealer/store_info.html', {'store': store, 'cars': cars})
