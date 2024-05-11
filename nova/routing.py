from django.urls import path

from core import consumers

urlrouter = [
    path('counters/', consumers.CountersConsumer.as_asgi()),
]
