from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse # Django Framework response
from django.db.models import F, Count
from rest_framework.decorators import api_view # Rest Framework
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

# Create your views here.
@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        # select related is used to reduce the no. of queries by joining the tables "collection and product" using INNER JOIN
        query_set = Product.objects.select_related('collection').all() # this is 1st 2nd 3rd way for serializing relationship
        
        # serializer = ProductSerializer(query_set, many=True) # this is okay but below used for 4th way of serializing relationship.
        
        serializer = ProductSerializer(query_set, many=True, context={'request': request})
        return Response(serializer.data) # this will return the data in Json Format
    
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # this is same as above but raise_exception is used to raise exception if serializer is not valid
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET", "PUT", "DELETE"])
def product_details(request, id):
    product = Product.objects.get(pk=id)
    if request.method == "GET":
        try:
            serializer = ProductSerializer(product)
            return Response(serializer.data) # this will return the data in Json Format
        except Product.DoesNotExist:
            # return Response(status=404) # this is simple 404 error response, we have to write codes for every error.
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data) # sending the product which need to be updated.
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "DELETE":
        if product.orderitems.count() > 0:
            return Response({"error": "The product is associate with order items"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response({"success": "The product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
# This is same as above but handled error by get_object_or_404
# @api_view()
# def product_details(request, id):
#     product = get_object_or_404(Product, pk=id)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data) # this will return the data in Json Format

@api_view(["GET", "DELETE", "PUT"])
def collection_details(request, pk):
    collection = Collection.objects.annotate(products_count = Count("products")).get(pk=pk)
    if request.method == "GET":
        try:
            serializer = CollectionSerializer(collection)
            return Response(serializer.data)
        except Collection.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    elif request.method == "PUT":
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
        
    elif request.method == "DELETE":
        if collection.products.count() > 0:
            return Response({"error": "The collection is associated with products"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["GET", "POST"])
def collection_list(request):
    if request.method == "GET":
        collection = Collection.objects.annotate(products_count = Count("products"))
        serializer = CollectionSerializer(collection, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)