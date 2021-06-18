from rest_framework import status, views, viewsets, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from commons.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from knox.auth import TokenAuthentication

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from .serializers import OrderHistorySerializer, OrderSerializer
from .models import Order, OrderHistory
from .helper import PlaceOrders, DeleteOrder
from restaurant.models import Kitchen, Item

from concurrent.futures import ThreadPoolExecutor

User = get_user_model()
executor = ThreadPoolExecutor()

class OrderObject(object):
    lookup = 'pk'

    def get_item_order(self):
        pk = self.kwargs.get(self.lookup)
        obj = None
        if id is not None:
            item = get_object_or_404(Item, pk=pk)
            user = self.request.user
            kitchen_name = item.kitchen
            order = Order.objects.filter(
                user = user, 
                kitchen_name = kitchen_name, 
                order_placed=False)

            context = {'order':order, 'item':item}
            return context


class CartOrderView(OrderObject, viewsets.ViewSet):
    order = Order.objects.all().order_by('-id')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    
    def get_queryset(self):
        user = self.request.user
        return Order.objects.select_related('user').filter(user=user).order_by('-id')   

    def add_item(self, request, pk=None, *args, **kwargs):
        order = self.get_item_order()['order']
        item = self.get_item_order()['item']
        user = self.request.user

        func = PlaceOrders(order, item, pk, user)
        thread = executor.submit(func.add)
        result = thread.result()
        return Response(result, status=status.HTTP_201_CREATED)


    def decrease(self, request, pk=None, *args, **kwargs):
        order = self.get_item_order()['order']
        item = self.get_item_order()['item']
        user = self.request.user
        
        func = DeleteOrder(order, item, pk, user)
        thread = executor.submit(func.delete_item)
        result = thread.result()
        return Response(result, status=status.HTTP_200_OK)


    def get_order(self, request, pk=None, *args, **kwargs):
        qs = Order.objects.select_related('user').filter(id = pk)
        return Response(OrderSerializer(qs, many=True).data)



class OrderHistoryView(viewsets.ModelViewSet):

    serializer_class = OrderHistorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    http_method_names = ['get']

    def get_queryset(self):
        return OrderHistory.objects.select_related().filter(user = self.request.user)


    @action(methods=['get'], detail=False)
    def today_orders(self, request):
        orders = Order.objects.select_related('user').filter(user = self.request.user, order_placed=True).filter(order_date=date.today())
        seri = OrderSerializer(orders, many=True).data
        if seri :
            return Response(seri)
        return Response("No orders found ! Please make a successful order to view history")

    @action(methods=['get'], detail=False)
    def past_orders(self, request):
        orders = Order.objects.select_related('user').filter(user = self.request.user, order_placed=True).filter(order_date__lt=date.today())
        seri = OrderSerializer(orders, many=True).data
        if seri :
            return Response(seri)
        return Response("No orders found on back date! Make an order to suit yourself")

    @action(methods=['get'], detail=False)
    def future_orders(self, request):
        orders = Order.objects.select_related('user').filter(user = self.request.user, order_placed=True).filter(order_date__gt=date.today())
        seri = OrderSerializer(orders, many=True).data
        if seri :
            return Response(seri)
        return Response("No orders found on future date! Make an order to suit yourself")


#---------------------------------------
