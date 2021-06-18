from django.urls import path, include
from rest_framework import routers

from .views import FeebackView, Refer_EarnView, KitchenRequestView



app_name = 'review'

router = routers.DefaultRouter()
router.register(r'kitchen_request', KitchenRequestView, basename='kitchen_request')

urlpatterns = [

    path('feedback/', FeebackView.as_view({'post':'create'}), name='feedback'),
    path('', include(router.urls)),   
    path('customer_refferal_data/', Refer_EarnView.as_view({'get':'get_my_customer_ref_data'}), name='customer_refferal_data'),
]