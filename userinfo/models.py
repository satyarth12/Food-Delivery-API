from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from PIL import Image

from django.contrib.auth import get_user_model
from account.proxy_models import Customer, Vendor
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .managers import CommentManager

from django.utils.translation import ugettext_lazy as _

User = get_user_model()



class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 200)
    about = models.TextField(blank=True, null=True)
    email = models.EmailField(_("Email Address"), max_length = 254, null=True, blank=True)
    image = models.ImageField(upload_to='customer/profile_images/', null=True, blank=True)

    def __str__(self):
        return f'{self.user}'


@receiver(post_save, sender=Customer)
def create_customerprofile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user = instance.user)




class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 200)
    about = models.TextField(blank=True, null=True)
    email = models.EmailField(_("Email Address"), max_length = 254, null=True, blank=True)
    image = models.ImageField(upload_to='vendor/profile_images/', null=True, blank=True)

    def __str__(self):
        return f'{self.user}'


@receiver(post_save, sender=Vendor)
def create_vendorprofile(sender, instance, created, **kwargs):
    if created:
        VendorProfile.objects.create(user = instance.user)







class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user} comment thread on {self.content_type}-{self.object_id}'

    def children(self): #replies
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True




add_type = (
    ('HOME', 'Home'),
    ('WORK', 'Work'),
    ('HOTEL','Hotel'),
    ('OTHER','OTHER')
    )

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    complete_address = models.CharField(max_length=200,  null=True, blank=True)
    landmark = models.CharField(max_length=200,  null=True,blank=True)
    address_type = models.CharField(max_length=200,  null=True, default=add_type[0], choices = add_type)
    city = models.CharField(max_length=200,  null=True, blank=True)

    pincode = models.CharField(max_length=200,  null=True, help_text="Be very specific and correct with your pincode")
   
    active = models.BooleanField(default=True, help_text = "User will get near by kitchen on the active address only")
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'User {self.user}-{self.pincode}'



@receiver(post_save, sender=UserAddress)
def create_useraddress(sender, instance, created, **kwargs):
    all_address = UserAddress.objects.select_related('user').filter(user = instance.user).exclude(id = instance.id)
    if created:
        for add in all_address:
            add.active = False
            add.save()
