![workflow](https://github.com/co01l3r/car_dealer/actions/workflows/django.yml/badge.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/co01l3r/car_dealer)

# car_dealer

a simple car dealer app, with possibility to buy and sell cars of particular make and model for a price to a store, or buy from it.

app stores transaction details with some basic math operations useful for the store

#### how to use:
```virtualenv```
```python
$ virtualenv <env_name>
$ source <env_name>/bin/activate
(<env_name>) $ pip install -r path/to/requirements.txt

from project folder:

(<env_name>) $ python3 manage.py runserver
```

or via ```Docker```:

```shell
$ docker-compose up --build
```
alternatively, if you have a container already build-up:

```shell
$ docker-compose up
```
project will then be available at these hosts under port ```0.0.0.0:8000```:

available API endpoints:
```shell
[
        '/api/stores',
        '/api/stores/<int:pk>',

        '/api/cars',
        '/api/car_list/?ordering=ORDERING_OPTION>',
        '/api/cars/submit',
        '/api/cars/<int:pk>/buy',

        '/api/transactions/',
        '/api/transactions/summary',
    ]
```