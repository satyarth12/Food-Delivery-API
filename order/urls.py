from django.urls import path, include
from . import views, payment
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'order-history', views.OrderHistoryView, basename='order-history')

app_name = 'order'


urlpatterns = [
	
	path('', include(router.urls)),

	path('get_order/<int:pk>/',views.CartOrderView.as_view({'get':'get_order'}), name='cartorder'),
    path('add_order/<int:pk>/',views.CartOrderView.as_view({'post':'add_item'}), name='cartorder'),   
    path('decrease/<int:pk>/quantity/', views.CartOrderView.as_view({'put':'decrease'}), name='ItemQuantity'),

    path('pay/<int:pk>/',payment.InitiatePayment.as_view({'post':'pay'}), name='pay'),
    path('handlepayment/', payment.InitiatePayment.as_view({'post':'handlepayment'}), name='callback'),


]