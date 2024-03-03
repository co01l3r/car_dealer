from django.urls import path
from . import views

urlpatterns = [
    path('submit_car/', views.submit_car, name='submit_car'),
    path('buy_car/<int:car_id>/', views.buy_car, name='buy_car'),
    path('store_info/', views.store_info, name='store_info'),
    path('', views.car_list, name='car_list'),
]
