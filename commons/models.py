from django.db import models

class BaseClass(models.Model):
    # record_id = models.AutoField(primary_key=True, help_text='common primary key for all the tables')
    created_by = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=256, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

