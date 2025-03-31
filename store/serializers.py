from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection, Reviews, Order, OrderItem, Cart, CartItem, Customer

# these serializers are used to convert data into JSON format
# It doesnot neceassary to add all fields of model in serializer
# Just add the fields you want to displaty in JSON format

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]
        
    products_count = serializers.IntegerField() # this is a custom field
        
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)

class ProductSerializer(serializers.ModelSerializer): # class ProductSerializer(serializers.Serializer):
    # since we are using ModelSerializer we dont need to define the fields explicitly
    # we are doing donkey work by defining double in model class and in serailizer class so using model serializer.
    class Meta:
        model = Product
        # fields = "__all__" # return all fields for lazy developers
        fields = ["id", "title", "description", "slug", "inventory", "unit_price", "price_with_tax", "collection"]
        
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source="unit_price")
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    
    # this cuses 1000 of queries if select related is not used in views.py
    # this is 1st way for serializing relationship
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )
    
    # this is 2nd way for serializing relationship
    # collection = serializers.StringRelatedField()
    
    # this is 3rd way for serializing relationship
    # collection = CollectionSerializer()
    
    # this is 4th way for serializing relationship
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name = "collection_details"
    # )
    
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
    # these things done by serializer save() method
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return super().create(validated_data)
    
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get("unit_price")
    #     instance.save()
    #     return super().update(instance, validated_data)
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ["id", "name", "description", "date"]
    
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Reviews.objects.create(product_id=product_id, **validated_data)
        