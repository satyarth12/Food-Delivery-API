from django.db import models
from commons import models as common
from django.core.validators import RegexValidator

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)

from account.proxy_models import Customer, Vendor
from django.core.exceptions import ValidationError

from taggit.managers import TaggableManager
from utils.models import Timestamps
from geopy.geocoders import Nominatim

from userinfo.models import Comment
from .managers import KitchenModelManager, KitchenCuisineModelManager, ItemModelManager

User = get_user_model()

kit_sts = (
    ('OPEN','open'),
    ('BUSY','busy'),
    ('CLOSE','close')
    )


class Kitchen(Timestamps):
    kitchen_name = models.CharField(max_length=100)
    about = models.TextField(null=True, blank=True)

    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)

    delivery = models.BooleanField(default=False)
    takeaway = models.BooleanField(default=False)

    veg = models.BooleanField(default=False)
    nonveg = models.BooleanField(default=False)

    menu_image = models.ImageField(upload_to='files/menu/', null=True, blank=True)
    kitchen_image = models.ImageField(upload_to='files/kitchen_image/', null=True, blank=True)
    kitchen_welcome_text = models.TextField(blank=True, null=True)
    
    likes = models.ManyToManyField(User, related_name="Kitchen_likes", blank=True)
    kitchen_status = models.CharField(max_length=100, blank=True, null=True, choices=kit_sts, default=kit_sts[0])
    user =  models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null = True, help_text="Select user who is vendor.")

    objects = KitchenModelManager()

    def save(self, *args, **kwargs):
        curr_user = get_current_authenticated_user()
        if Vendor.objects.filter(phone = curr_user).exists():
            if not self.user:
                self.user = curr_user
            super(Kitchen, self).save(*args, **kwargs)
        else:
            raise ValidationError("You are not the vendor")

    def __str__(self):
        return self.kitchen_name




class KitchenAdress(models.Model):
    kitchen = models.OneToOneField(Kitchen, on_delete=models.CASCADE, related_name='kitchen_address')

    address = models.TextField(blank=True, null=True)
    area = models.CharField(max_length=256, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)


    pincode = models.CharField(max_length=150)
    latitude = models.CharField(max_length=256, null=True, blank=True)
    longitude = models.CharField(max_length=256, null=True, blank=True)


    def save(self, *args, **kwargs):
        geolocator = Nominatim(user_agent = "geoapiExercises")
        location = geolocator.geocode(int(self.pincode))
        self.latitude = location.latitude
        self.longitude = location.longitude
        super(KitchenAdress, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.kitchen}'






class KitchenCuisine(Timestamps):
    kitchen = models.OneToOneField(Kitchen, null=True, blank=True, on_delete=models.CASCADE, related_name='categories')

    cuisine_names=TaggableManager(help_text="What's the kitchen main cuisines? Not more than 5.", blank=True)
    kitchen_ranking = models.CharField(max_length=100, null=True, blank=True, help_text="Rank kitchen according to their popluraity.")

    objects = KitchenCuisineModelManager()

    def save(self, *args, **kwargs):
        curr_user = get_current_authenticated_user()
        curr_user_kitchen = Kitchen.objects.select_related('user').filter(user = curr_user).first()
        if curr_user_kitchen and not self.kitchen:
            self.kitchen = curr_user_kitchen
        super(KitchenCuisine, self).save(*args, **kwargs)

    def __str__(self):
        return f'Cuisine for {self.kitchen}'


@receiver(post_save, sender=Kitchen)
def create_kitchencuisine(sender, instance, created, **kwargs):
    if created:
        KitchenCuisine.objects.create(kitchen = instance)





class Category(Timestamps):
    kitchen = models.ForeignKey(Kitchen, null=True, blank=True , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='category/images/', null=True, blank=True)
    category_name = TaggableManager(help_text="Enter Category for an Item. Create only if the category is not pre-present.")
    about = models.TextField(null=True)

    def save(self, *args, **kwargs):
        curr_user = get_current_authenticated_user()
        curr_user_kitchen = Kitchen.objects.select_related('user').filter(user = curr_user).first()
        if curr_user_kitchen and not self.kitchen:
            self.kitchen = curr_user_kitchen
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        for tag in self.category_name.all():
            return f'{tag}'



class Item(Timestamps):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    kitchen = models.ForeignKey(Kitchen, on_delete=models.SET_NULL, null=True, related_name='items')

    name = models.CharField(blank=False, max_length=256)
    cost = models.CharField(blank=False, max_length=15)
    desc = models.TextField(null=True, blank=True)
    ingredients = models.TextField()

    total_order_placed = models.IntegerField(default = 0, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name = 'Kitchen_Item', blank=True)

    image = models.ImageField(upload_to='files/item/', max_length=1023, null=True, blank=True, verbose_name='Image 1')
    image_2 = models.ImageField(upload_to='files/item/', max_length=1023, null=True, blank=True, verbose_name='Image 2')
    delivery_time = models.CharField(max_length=10, null=True, blank=True, verbose_name="Cooking Time")
    is_available = models.BooleanField(default=True)

    objects = ItemModelManager()
    
    def save(self, *args, **kwargs):
        curr_user = get_current_authenticated_user()
        curr_user_kitchen = Kitchen.objects.select_related('user').filter(user = curr_user).first()
        if curr_user_kitchen and not self.kitchen:
            self.kitchen = curr_user_kitchen
        super(Item, self).save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    def __str__(self):
        return f'{self.name} from kitchen {self.kitchen}'


    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type






