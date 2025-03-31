from django.urls import path
# from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers
from . import views

# router = SimpleRouter()
# router.register("products", views.ProductViewSet)
# router.register("collections", views.CollectionViewSet)

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="prod") # this is used for reverse routing
router.register("collections", views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router, "products", lookup = "ye") # this will search for product_pk could be any name 
products_router.register("reviews", views.ReviewViewSet, basename = "product-reviews") # this product-reviews used for reverse routing

# urlpatterns = [
#     path("products", views.ProductList.as_view()),
#     path("products/<int:pk>", views.ProductDetails.as_view()), # if simple <id> then any character can be passed but product id is int only field
#     path("collections/<int:pk>", views.CollectionDetails.as_view(), name='collection_details'),
#     path("collections", views.collection_list),
# ]

urlpatterns = router.urls + products_router.urls
