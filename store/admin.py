from django.contrib import admin

from django.db.models import F, Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

# Register your models here.

# admin.site.register(models.Product, ProductAdmin)

class InventoryFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name = "inventory" # this is key for the query string parameter, right now we are not using it just the value we are concerned with
    
    def lookups(self, request, model_admin):
        return [
            ("<10", "Low"),
            (">=10", "OK")
        ]
    
    def queryset(self, request, queryset):
        if self.value() == "<10":
            return queryset.filter(inventory__lt = 10)
        elif self.value() == ">=10":
            return queryset.filter(inventory__gte = 10)
        else:
            return queryset



@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    autocomplete_fields = ["collection"]
    prepopulated_fields = {
        "slug": ["title"]
    }
    actions = ["clear_inventory"]
    
    list_display = ["title", "unit_price", "inventory_status", "collection_title"] 
    ''' 
    this collection_title is just to show that we can show any field of the related model
    in the display by defining a function with the name
    and since __str__ is defined for title so for other field we need to do this.
    '''
    list_editable = ["unit_price"]
    list_per_page = 10
    list_select_related = ["collection"] # this is for selecting the related model -> collection title will cause thousand of queries otherwise
    list_filter = ["collection", "last_update", InventoryFilter] # this is for filtering the data
    
    def collection_title(self, obj):
        return obj.collection.title
    
    @admin.display(ordering="inventory") # for odering this column on inventory value
    def inventory_status(self, obj): # a computed column
        if obj.inventory < 10:
            return "Low"
        return "OK"
    
    @admin.action(description="Clear Inventory") # the text shown in drop down list
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated'
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership", "orders_count"]
    list_editable = ["membership"]
    list_per_page = 10
    ordering = ["first_name", "last_name"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]
    
    @admin.display(ordering="orders_count")
    def orders_count(self, obj):
        url = (reverse('admin:store_order_changelist') 
               + '?'
               + urlencode({
                   "customer__id": str(obj.id)
               }))
        return format_html('<a href="{}">{}<a/>' , url, obj.orders_count)
        # return obj.orders_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count = Count("order"))
    
class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ["product"]
    model = models.OrderItem
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer"]
    inlines = [OrderItemInline]
    list_display = ["id", "placed_at", "customer"]
    list_per_page = 10

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "products_count"]
    
    @admin.display(ordering="products_count")
    def products_count(self, obj):
        url = (reverse('admin:store_product_changelist') 
               + '?'
               + urlencode({
                   "collection__id": str(obj.id)
               }))
        
        return format_html('<a href="{}">{}<a/>' , url, obj.products_count)
        # return obj.products_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count = Count("product"))