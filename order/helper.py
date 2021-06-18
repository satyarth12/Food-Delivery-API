import json

from django.contrib.auth import get_user_model
from .serializers import OrderSerializer, OrderHistorySerializer

from concurrent.futures import ThreadPoolExecutor
import os

User = get_user_model()
executor = ThreadPoolExecutor()


class PlaceOrders:
    def __init__(self, order, item, pk, curr_user):
        self.order = order
        self.item = item
        self.pk = pk
        self.curr_user = curr_user


    def increase(self):
        for key in self.order.item_names.keys():
            if str(key) == str(self.pk):
                count = self.order.item_names[key][1] + 1

                self.order.item_names[key][1] = count
                self.order.item_names[key][2] = int(self.item.cost)*count
                self.order.order_total = int(self.order.order_total) + int(self.item.cost)
        
                return self.order.save()


    def add(self):
        if self.order.exists(): 
            self.order = self.order.first()
            new_item = []
            item_count = 1

           
            if str(self.pk) in self.order.item_names.keys():
                executor.submit(self.increase(), self.order, self.item, self.pk, self.curr_user)
                return 'Item Increased'


            new_item.append(self.item.name)
            new_item.append(item_count)
            new_item.append(self.item.cost)

            self.order.item_names[self.item.id] = new_item
            self.order.total_items = len(self.order.item_names)

            total_cost=0
            for key,values in self.order.item_names.items():
                total_cost += int(values[2])

            self.order.order_total = total_cost

            data = {'user':self.order.user.id, 
                    'kitchen_name':self.order.kitchen_name.id, 
                    'item_names': self.order.item_names, 
                    'total_items':len(self.order.item_names),
                    'order_total':total_cost} 
            self.order.save()
            return data


        new_item = [] 
        self.item_count = 1
        new_item.append(self.item.name)
        new_item.append(self.item_count)
        new_item.append(self.item.cost)

        new_list = {self.item.id:new_item}

        data = {'user':self.curr_user.id, 
                'kitchen_name':self.item.kitchen.id, 
                'item_names':new_list, 
                'total_items':1, 
                'order_total':self.item.cost}
        serializer = OrderSerializer(data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return serializer.data




class DeleteOrder:
    def __init__(self, order, item, pk, curr_user):
        self.order = order
        self.item = item
        self.pk = pk
        self.curr_user = curr_user


    def delete_item(self):
        if self.order.exists():
            order = self.order.first()

            for key in order.item_names.keys():
                if str(key) == str(self.pk):

                    count = order.item_names[key][1] - 1

                    if count == 0:
                        order.item_names.pop(key)
                        new = order.item_names
                        total = int(order.order_total)
                        cost = int(self.item.cost)

                        if bool(new) == False:
                            order.delete()
                            return 'Order Removed'

                        order.item_names = new
                        order.order_total = total-cost
                        order.total_items = len(new)
                        order.save()
                        return 'Item Removed'


                    total = int(order.order_total)
                    cost = int(self.item.cost)
                    order.order_total = total-cost

                    order.item_names[key][1] = count
                    order.item_names[key][2] = str(cost*count)
                    
                    order.save()
                    return 'Decreased'

        # return Response('Error in Order', status=status.HTTP_404_NOT_FOUND)

