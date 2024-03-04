from django.urls import path
from .views import (
    store_list_create_api_view,
    submit_car_for_purchase,
    purchase_car,
    get_store_with_cars,
    car_list,
    transactions_summary,
    transaction_list,
    get_routes,
)

urlpatterns = [
    path('', get_routes),
    path('stores/', store_list_create_api_view, name='store-list-create'),
    path('stores/<int:pk>/', get_store_with_cars, name='store-detail'),
    path('cars/', car_list, name='car-list'),
    path('cars/submit/', submit_car_for_purchase, name='car-submit'),
    path('cars/<int:pk>/buy/', purchase_car, name='car-buy'),
    path('transactions/summary/', transactions_summary, name='transaction-summary'),
    path('transactions/', transaction_list, name='transaction-list'),
]
