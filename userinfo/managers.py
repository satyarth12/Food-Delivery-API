from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id= obj_id) #.filter(parent=None)
        return qs

    def create_by_modeltype(self, model_type, pk, content, user, parent_obj=None):
        model_qs = ContentType.objects.filter(model = model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id = pk)
            if not obj_qs.exists() or obj_qs.count() == 1:
                instance = self.model()
                instance.content = content
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                instance.user = user
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None