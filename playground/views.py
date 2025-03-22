from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, Count
from django.contrib.contenttypes.models import ContentType
from store.models import Product, OrderItem, Order, Customer
from tags.models import Tag, TaggedItem

# Create your views here.
def say_hello(request):
    # query_set = Product.objects.filter(unit_price__range=(20,30))
    # query_set = Order.objects.order_by("-placed_at")[:5].select_related("customer").prefetch_related("orderitem_set__product")
    # query_set = Customer.objects.annotate(order_count = Count("order"))
    
    # content = ContentType.objects.get_for_model(Product)
    # query_set = TaggedItem.objects.filter(content_type = content, object_id = 1).select_related("tag")
    query_set = TaggedItem.objects.get_tags_for(Product, 1) # this object is the manager object
    
    # print(query_set)
    return render(request, "hello.html", {"name": "Mosh!!", "orders": query_set})

def collection_range(request):
    # query_set = Product.objects.filter(collection__id__range=(20,30))
    query_set = Product.objects.values("collection__id", "title", "collection__title")
    # print(query_set)
    return render(request, "hello.html", {"name": "Hunaaza!!", "products": query_set})

def inventory_collection(request):
    query_set = Product.objects.filter(inventory = F('collection_id'))
    return render(request, "hello.html", {"name": "Mosh!!", "products": query_set})

def get_orderitem(request):
    query_set = OrderItem.objects.values("product__id").distinct()
    products = Product.objects.filter(id__in = query_set).order_by('title')
    return render(request, "hello.html", {"name": "Mosh!!", "products": products})