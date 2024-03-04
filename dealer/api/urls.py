from django.urls import path
from .views import store_list_create_api_view, submit_car, buy_car, store_info, car_list, transactions_summary, transaction_list

urlpatterns = [
    path('stores/', store_list_create_api_view, name='store-list-create'),
    path('submit_car/', submit_car, name='submit-car'),
    path('buy_car/<int:car_id>/', buy_car, name='buy-car'),
    path('store_info/', store_info, name='store-info'),
    path('car_list/', car_list, name='car_list'),
    path('transactions_summary/', transactions_summary, name='transactions_summary'),
    path('transactions/', transaction_list, name='transaction-list'),
]
