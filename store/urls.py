from django.urls import path
from . import views

urlpatterns = [
    path("products", views.product_list),
    path("products/<int:id>", views.product_details), # if simple <id> then any character can be passed but product id is int only field
    path("collections/<int:pk>", views.collection_details, name='collection_details'),
    path("collections", views.collection_list),
]
