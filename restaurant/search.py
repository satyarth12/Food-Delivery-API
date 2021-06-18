from django.contrib.auth import get_user_model
from rest_framework import permissions, status, views, viewsets, generics
from rest_framework.response import Response
from itertools import chain

from restaurant.models import Kitchen, KitchenCuisine, Item, KitchenAdress
from restaurant.serializers import KitchenSerializer
from .utils import check_address_distance

from django.shortcuts import get_object_or_404
from commons.permissions import IsOwnerOrReadOnly, IsKitchenOwnerOrReadOnly
from taggit.models import Tag



class SearchKitchenName(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = KitchenSerializer
   
    def kitchen_by_multimodel(self, *args, **kwargs):
        query = self.request.GET.get('kitchen-item-cuisine')
        if query != '' and query is not None:

            kitchen_result = Kitchen.objects.select_related().search(query)
            kitchen_cui_result = KitchenCuisine.objects.select_related().search(query)
            item_result = Item.objects.select_related().search(query)

            kitch_cui = []
            for KI in kitchen_cui_result.iterator():
                kitch_cui.append(KI.kitchen)

            item_kitch = []
            for i in item_result.iterator():
                item_kitch.append(i.kitchen)

            queryset_chain= chain(kitchen_result,
                                kitch_cui,
                                item_kitch)
            print(queryset_chain)

            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
            return Response(KitchenSerializer(qs, many=True).data)
        return Response('Type to search')


    def pureveg_kitchen(self, request):
        qs = Kitchen.objects.select_related().filter(veg=True, nonveg=False)
        kitchen = KitchenSerializer(qs, many=True).data
        return Response(kitchen)


    def nonveg_kitchen(self, request):
        qs = Kitchen.objects.select_related().filter(veg=False, nonveg=True)
        kitchen = KitchenSerializer(qs, many=True).data
        return Response(kitchen)


    def pincode_kitchen(self, *args, **kwargs):
        query = self.request.GET.get('pincode')
        if query != '' and query is not None:
            user_address = query
            kitchen_address = KitchenAdress.objects.all().select_related('kitchen')

            if user_address:
                payload = check_address_distance(user_address, kitchen_address)
                qs = Kitchen.objects.filter(pk__in = payload)
                if qs:
                    kitchen = KitchenSerializer(qs, many=True).data
                    return Response(kitchen)
                return Response("No kitchen found in radius of this pincode")
            return Response("Please enter a correct pincode")
        return Response('Type to search')
