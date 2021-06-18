from django.urls import path, include
from rest_framework import routers
from .views import CustomerProfileView, VendorProfileView, CommentListView, CommentDetailView, CommentCreateView, UserAddressView


app_name = 'userinfo'

router = routers.DefaultRouter()
router.register(r'customerprofile', CustomerProfileView, basename = "customerprofile")
router.register(r'vendorprofile', CustomerProfileView, basename = "vendorprofile")
router.register(r'useraddress', UserAddressView, basename = "useraddress")

urlpatterns = [
    path('', include(router.urls)),
    path('comment/', CommentListView.as_view(), name = 'comment'),
    path('comment/create/', CommentCreateView.as_view(), name = 'comment-create'),
    path('comment/<int:pk>/', CommentDetailView.as_view(), name = 'thread'),

]
