from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse # Django Framework response
from rest_framework.decorators import api_view # Rest Framework
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

# Create your views here.
@api_view()
def product_list(request):
    # select related is used to reduce the no. of queries by joining the tables "collection and product" using INNER JOIN
    query_set = Product.objects.select_related('collection').all() # this is 1 way for serializing relationship
    
    # serializer = ProductSerializer(query_set, many=True) # this is okay but below used for 3rd way of serializing relationship.
    
    serializer = ProductSerializer(query_set, many=True, context={'request': request})
    return Response(serializer.data) # this will return the data in Json Format

@api_view()
def product_details(request, id):
    try:
        product = Product.objects.get(pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data) # this will return the data in Json Format
    except Product.DoesNotExist:
        # return Response(status=404) # this is simple 404 error response, we have to write codes for every error.
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# This is same as above but handled error by get_object_or_404
# @api_view()
# def product_details(request, id):
#     product = get_object_or_404(Product, pk=id)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data) # this will return the data in Json Format

@api_view()
def collection_details(request, pk):
    return Response("OK")
