from django.urls import path
from . import views

urlpatterns = [
    path("hello", views.say_hello),
    path("hunaiza", views.collection_range),
    path("Inventory", views.inventory_collection),
    path("get_order", views.get_orderitem),
]
