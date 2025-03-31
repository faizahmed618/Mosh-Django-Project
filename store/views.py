from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse # Django Framework response
from django.db.models import F, Count
from django_filters.rest_framework import DjangoFilterBackend # for generic filtering

from rest_framework.filters import SearchFilter, OrderingFilter # for text field searching
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view # Rest Framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Product, Collection, OrderItem, Reviews
from .filters import ProductFilter
from .pagination import CustomPagination
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer

# Create your views here.
class ProductViewSet(ModelViewSet): # viewset contain all the individual mixin that present in generics class so using viewsets we can reduce the code.
    queryset = Product.objects.all() # this line
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ["collection_id"]
    filterset_class = ProductFilter # this is used to filter the data using the filterset class defined in filters.py file.
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]
    
    pagination_class = CustomPagination
    
    
    def get_serializer_context(self): # we dont have attribute for serializer context so we have to over write this method.
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs["pk"]).count() > 0:
            return Response({"error": "The product is associate with order items"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    # def get_queryset(self): # this is same write above line or this
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get("collection_id", None) # this is used to filter the products by collection id.
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset
    
    # Since this will show delete button in the list view too so we just overwrite the destroy method.
    # Since there is no delete method in the viewset so we have to overwrite the destroy method.
    # otherwise it will show delete button in the list view too.
    
    # def delete(self, request, pk): # using the delete method to overwrite since our one is customized.
    #     product = self.queryset.get(pk=pk)
    #     if product.orderitems.count() > 0:
    #         return Response({"error": "The product is associate with order items"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response({"success": "The product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ProductList(ListCreateAPIView):
    # this is same as below class ProductList(APIview) but using class based view.
    # def get(self, request):
    #     query_set = Product.objects.select_related('collection').all()
    #     serializer = ProductSerializer(query_set, many=True, context={'request': request})
    #     return Response(serializer.data)
    
    # def post(self,request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    #########################################################################################################
    # these are for generic views
    queryset = Product.objects.select_related('collection').all() # this line
    serializer_class = ProductSerializer
    
    # def get_queryset(self): # this is same write above line or this 
    #     return Product.objects.select_related('collection').all()
    
    def get_serializer_context(self): # we dont have attribute for serializer context so we have to over write this method.
        return {'request': self.request}

@api_view(["GET", "POST"]) # see above class ProductList(APIview) is same using class based view
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

class ProductDetails(RetrieveUpdateDestroyAPIView):
    # this is same as below class ProductList(APIview) but using class based view
    def get_object_local(self, id):
        return get_object_or_404(Product, pk=id)
    
    # def get(self, request, id):
    #     product = self.get_object(id)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)
    
    # def put(self, request, id):
    #     product = self.get_object(id)
    #     serializer = ProductSerializer(product, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk): # using the delete method to overwrite since our one is customized.
        product = self.get_object_local(pk)
        if product.orderitems.count() > 0:
            return Response({"error": "The product is associate with order items"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response({"success": "The product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    ######################################################################################################
    queryset = Product.objects.all() # this line
    serializer_class = ProductSerializer
    
    
@api_view(["GET", "PUT", "DELETE"])# see above class ProductDetails(APIview) is same using class based view
def product_details(request, pk):
    product = Product.objects.get(pk=pk)
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
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    elif request.method == "DELETE":
        if collection.products.count() > 0:
            return Response({"error": "The collection is associated with products"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionDetails(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count = Count("products"))
    serializer_class = CollectionSerializer
    
    def delete(self, request, pk): # using the delete method to overwrite since our one is customized.
        # collection = Collection.objects.get(pk=pk)
        # collection = CollectionDetails.queryset.get(pk=pk) # this is same as above line.
        collection = self.queryset.get(pk=pk) # this is same as above line.
        if collection.products.count() > 0:
            return Response({"error": "The collection is associate with products"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response({"success": "The collection deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
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
    
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count = Count("products"))
    serializer_class = CollectionSerializer
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count = Count("products"))
    serializer_class = CollectionSerializer
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs["pk"]).count() > 0:
            return Response({"error": "The collection is associate with products"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    # def delete(self, request, pk): # using the delete method to overwrite since our one is customized.
    #     collection = self.queryset.get(pk=pk) # this is same as above line.
    #     if collection.products.count() > 0:
    #         return Response({"error": "The collection is associate with products"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response({"success": "The collection deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class ReviewViewSet(ModelViewSet):
    # queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Reviews.objects.filter(product_id=self.kwargs["ye_pk"])
    
    def get_serializer_context(self):
        return {"product_id": self.kwargs["ye_pk"], "request": self.request}
    
    

