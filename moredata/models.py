from django.db import models
from utils.models import Timestamps
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from restaurant.models import Kitchen
from account.proxy_models import Customer, Vendor
from order.models import Order
from userinfo.models import CustomerProfile, VendorProfile
from utils.utils import generate_ref_code

User = get_user_model()


class Feedback(Timestamps):
    user = models.ForeignKey(User, related_name='Feedback', on_delete=models.CASCADE)
    feed = models.TextField()

    def __str__(self):
        return f'{self.user}'



class Refer_Earn_Customer(Timestamps):
    user =  models.OneToOneField(User, related_name='refer_earn_customer', on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="ref_by_customer")

    my_recommended_users = models.ManyToManyField(Customer, blank=True, related_name="my_recommended_customer")
    total_refer_money = models.IntegerField(default = 0, blank=True, null=True, help_text="50 rs redeemed at each order.")
    redeemed_money = models.IntegerField(default = 0, blank=True, null=True)

    redeem_on_orders = models.ManyToManyField(Order, blank=True)


    def __str__(self):
        return f'{self.user}'

    def get_recommended_profiles(self):
        qs = Refer_Earn_Customer.objects.select_related('recommended_by')
        my_recoms = []
        for r_e in qs:
            if r_e.recommended_by == self.user:
                my_recoms.append(r_e)
        return my_recoms

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        super(Refer_Earn_Customer, self).save(*args, **kwargs)


@receiver(post_save, sender=Customer)
def create_refer_earn_customer(sender, instance, created, **kwargs):
    if created:
        Refer_Earn_Customer.objects.create(user = instance.user)




class Refer_Earn_Vendor(Timestamps):
    user =  models.OneToOneField(User, related_name='refer_earn_vendor', on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="ref_by_vendor")

    my_recommended_users = models.ManyToManyField(Vendor, blank=True, related_name="my_recommended_vendor")
    total_refer_money = models.IntegerField(default = 0, blank=True, null=True, help_text="50 rs redeemed at each order.")
    redeemed_money = models.IntegerField(default = 0, blank=True, null=True)

    def __str__(self):
        return f'{self.user}'

    def get_recommended_profiles(self):
        qs = Refer_Earn_Vendor.objects.select_related('recommended_by')
        my_recoms = []
        for r_e in qs:
            if r_e.recommended_by == self.user:
                my_recoms.append(r_e)
        return my_recoms

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        super(Refer_Earn_Vendor, self).save(*args, **kwargs)



@receiver(post_save, sender=Vendor)
def create_refer_earn_vendor(sender, instance, created, **kwargs):
    if created:
        Refer_Earn_Vendor.objects.create(user = instance.user)












class Verified_Kitchen(Timestamps):
    kitchen = models.OneToOneField(Kitchen, related_name = "verf_kitc", on_delete = models.CASCADE)
    verify  = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.kitchen}'




class KitchenRequest(Timestamps):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name="Requested_by")

    name = models.CharField(max_length=1000)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message='Phone number must be entered in the format: "9999999999".')
    phone = models.CharField(max_length=15, validators=[phone_regex])
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return f'Requested by {self.user}'
