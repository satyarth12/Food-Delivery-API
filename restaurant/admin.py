from django.contrib import admin
from .models import Kitchen, KitchenAdress, Item, KitchenCuisine, Category
from import_export.admin import ImportExportModelAdmin

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ("tag", "kitchen")

    def tag(self, obj):
        return u", ".join(o.name for o in obj.category_name.all())



@admin.register(Kitchen)
class KitchenAdmin(ImportExportModelAdmin):
    list_display = ("kitchen_name", "user", "kitchen_status")
    list_filter = ('veg','nonveg')


@admin.register(KitchenAdress)
class KitchenAdressAdmin(ImportExportModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin):
    pass


@admin.register(KitchenCuisine)
class KitchenCuisineAdmin(ImportExportModelAdmin):
    list_display = ("tag_list", "kitchen")

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.cuisine_names.all())