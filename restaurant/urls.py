from django.urls import path,include
from rest_framework import routers
from . import views, search

app_name = 'restaurant'
router = routers.DefaultRouter()
router.register(r'kitchen', views.KitchenView, basename='kitchen'),
router.register(r'kitchenaddress', views.KitchenAdressView, basename='kitchenaddress'),
router.register(r'kitchencuisine', views.KitchenCuisineView, basename='kitchencuisine'),
router.register(r'item', views.ItemView, basename='item'),
router.register(r'categorytags', views.CategoryTags, basename='categorytags'),



urlpatterns = [

    path('', include(router.urls)),

    path('cuisine/<str:slug>/kitchens/',views.KitchenInCuisineTags.as_view()),
    path('searchkitchen/name/', search.SearchKitchenName.as_view({'get':'kitchen_by_multimodel'})),
    path('searchkitchen/pureveg/', search.SearchKitchenName.as_view({'get':'pureveg_kitchen'})),
    path('searchkitchen/nonveg/', search.SearchKitchenName.as_view({'get':'nonveg_kitchen'})),
    path('searchkitchen/kitchen_by_pincode/', search.SearchKitchenName.as_view({'get':'pincode_kitchen'})),

]