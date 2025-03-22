from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
# A model is a class that represents a database table.

# Since id is the default primary key, we don't need to define it explicitly.
# Django will automatically add an id field to the model.
# The id field is an auto-incrementing integer field.
# We can override the default primary key by setting the primary_key attribute to True.
# In the Product model, we set the sku field as the primary key.
# This means that the sku field will be used as the primary key in the database table.

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True, related_name="+")
    # this + will not create a reverse relationship with product class
    
    def __str__(self): # this is a string representation of the object in the admin panel
        return self.title # when the object is printed this is implicitly called
    
    class Meta: # this is a meta class for ordering the items
        ordering = ["title"]
    
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # by default it create "product_set" but if we write related name = "products" it will create with this
    # Django handles the reverse relationship
    
class Product(models.Model):
    # sku = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, 
                                     decimal_places=2,
                                     validators=[MinValueValidator(1)])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT) # In case we delete the collection we dont delete the products
    promotions = models.ManyToManyField(Promotion)
    
    def __str__(self): # this is a string representation of the object in the admin panel
        return self.title # when the object is printed this is implicitly called
    
    class Meta: # this is a meta class for ordering the items
        ordering = ["title"]

    
class Customer(models.Model):
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, "Bronze"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_GOLD, "Gold"),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta: # this is a meta class for ordering the items
        ordering = ["first_name", "last_name"]
    
class Order(models.Model):
    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETE = "C"
    PAYMENT_STATUS_FAILED = "F"
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETE, "Complete"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True) 
    # we need single customer to have multiple addresses OnetoMany relation -> "Foreign Key"
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class OrderItem(models.Model):
    # reverse relationship with order with the name "orderitem_set" in order class
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    