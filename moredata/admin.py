from django.contrib import admin
from .models import Feedback, Refer_Earn_Customer, Refer_Earn_Vendor, Verified_Kitchen, KitchenRequest

admin.site.register(Feedback)

@admin.register(Verified_Kitchen)
class Verified_Kitchen_Admin(admin.ModelAdmin):
    list_display = ("kitchen", "verify")


@admin.register(Refer_Earn_Customer)
class Verified_Kitchen_Admin(admin.ModelAdmin):
    list_display = ("user","code","recommended_by")


@admin.register(Refer_Earn_Vendor)
class Verified_Kitchen_Admin(admin.ModelAdmin):
    list_display = ("user","code","recommended_by")



@admin.register(KitchenRequest)
class KitchenRequestAdmin(admin.ModelAdmin):
    list_display = ("user","name","city")