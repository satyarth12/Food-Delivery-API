from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from django.http import JsonResponse



User = get_user_model()

class KitchenQuerySet(models.QuerySet):
	def search(self, query=None):
		qs = self
		if query !=None and query is not None:
			lookup = (Q(kitchen_name__icontains=query))
			qs = qs.filter(lookup).distinct()
		return qs


class KitchenModelManager(models.Manager):
	def get_queryset(self):
		return KitchenQuerySet(self.model, using=self._db)

	def search(self, query=None):
		return self.get_queryset().search(query=query)





class KitchenCuisineQuerySet(models.QuerySet):
	def search(self, query=None):
		qs = self
		if query !=None and query is not None:
			query = query.split()
			lookup = (Q(cuisine_names__name__in=query))
			qs = qs.filter(lookup).distinct()
		return qs


class KitchenCuisineModelManager(models.Manager):
	def get_queryset(self):
		return KitchenCuisineQuerySet(self.model, using=self._db)

	def search(self, query=None):
		return self.get_queryset().search(query=query)





class ItemQuerySet(models.QuerySet):
	def search(self, query=None):
		qs = self
		if query !=None and query is not None:
			lookup = (Q(name__icontains=query))
			qs = qs.filter(lookup).distinct()
		return qs


class ItemModelManager(models.Manager):
	def get_queryset(self):
		return ItemQuerySet(self.model, using=self._db)

	def search(self, query=None):
		return self.get_queryset().search(query=query)