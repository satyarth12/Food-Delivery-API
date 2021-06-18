from django.contrib import admin
from .models import CustomerProfile, VendorProfile, Comment, UserAddress
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_type", "name")

    def user_type(self, obj):
    	user= User.objects.filter(phone = obj).first()
    	if user.is_customer == True:
            return 'Customer'



@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_type", "name")

    def user_type(self, obj):
        user= User.objects.filter(phone = obj).first()
        if user.is_vendor == True:
            return 'Vendor'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "content_type", "object_id", 'parent_detail')

    def parent_detail(self, obj):
        if obj.parent:
            return f'{obj.parent}'


admin.site.register(UserAddress)
