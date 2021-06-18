from django.db import models
from utils.models import Timestamps
from restaurant.models import Kitchen, Item
from django.contrib.auth import get_user_model

from django.utils.translation import ugettext_lazy as _
from account.proxy_models import Vendor

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE)
    kitchen_name = models.ForeignKey(Kitchen, related_name='Kitchen_Name', on_delete=models.CASCADE)

    item_names = models.JSONField()
    total_items = models.CharField(max_length=500, default=0)
    order_total = models.CharField(max_length=500, default=0, blank=True, null=True)

    order_placed = models.BooleanField(default=False, null=True, blank=False)

    order_date = models.DateField(null=True, blank=True, help_text="Date selected for the future order")
    order_slot_from = models.TimeField(null=True, blank=True, help_text="Time Slot selected for the future order delivery") 
    order_slot_to = models.TimeField(null=True, blank=True, help_text="Time Slot selected for the future order delivery") 

    def __str__(self):
    	return f'Kitchen Order {self.kitchen_name.kitchen_name} for user {self.user}'



class OrderHistory(models.Model):

    class Order_sts(models.TextChoices):
        accepted = 'ACCEPTED','Accepted',
        rejected = 'REJECTED', 'Rejected'

    user = models.ForeignKey(User, related_name='Order_User', on_delete=models.CASCADE, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    transaction_id = models.CharField(unique=True, max_length=100, null=True, blank=True)

    amount = models.IntegerField(blank=True, null=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    order_status = models.CharField(_("Order Status from Vendor"), max_length=50, choices=Order_sts.choices, default=Order_sts.accepted)
    delivery = models.BooleanField(_("Out for delivery"), default=False, null=True, blank=False)

    complete = models.BooleanField(default=False, null=True, blank=True)
    succes_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.transaction_id is None and self.created_at and self.id:
            self.transaction_id = self.created_at.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
    	return f'{self.order}'
