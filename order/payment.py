from rest_framework import status, views, viewsets, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from commons.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from knox.auth import TokenAuthentication

from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from main.paytm import generate_checksum, verify_checksum
from .models import Order, OrderHistory


class InitiatePayment(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def pay(self, request, pk=None, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)
        order_history = OrderHistory.objects.select_related('user').filter(order = order)

        if order_history.exists():
            return Response("Payement for this order is already done", status=status.HTTP_409_CONFLICT)

        if order.user == self.request.user:
            if order and order.order_placed == False:
                user = order.user
                vendor = order.kitchen_name.user
                amount = int(order.order_total)

                merchant_key = settings.PAYTM_SECRET_KEY

                params = (
                    ('MID', settings.PAYTM_MERCHANT_ID),
                    ('ORDER', str(order.id)),
                    ('VENDOR', str(vendor)),
                    ('CUST_ID', str(user)),
                    ('TXN_AMOUNT', str(amount)),
                    ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
                    ('WEBSITE', settings.PAYTM_WEBSITE),
                    # ('EMAIL', request.user.email),
                    # ('MOBILE_N0', '9911223388'),
                    ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
                    ('CALLBACK_URL', 'http://127.0.0.1:8000/order/handlepayment/'),
                    # ('PAYMENT_MODE_ONLY', 'NO'),
                )

                paytm_params = dict(params)
                checksum = generate_checksum(paytm_params, merchant_key)

                paytm_params['CHECKSUMHASH'] = checksum
                print('SENT: ', checksum)
                return Response(paytm_params)
        
            return Response('Either order is already placed or it does not exists', status=status.HTTP_400_BAD_REQUEST)
        return Response('Current user is unauthorized', status=status.HTTP_401_UNAUTHORIZED)


    def handlepayment(self, *args, **kwargs):

        received_data = dict(request.POST)
        paytm_params = {}
        order = None
        paytm_checksum = received_data['CHECKSUMHASH'][0]

        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
           
            elif key == 'ORDER':
                order = Order.objects.get(id=int(value[0]))

            elif key == 'CUST_ID':
                user = value[0]

            elif key == 'VENDOR':
                vendor = value[i]

            elif key == 'TXN_AMOUNT':
                amount = int(value[i])

        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))

        if is_valid_checksum:
            OrderHistory.objects.create(
                user=user, 
                vendor=vendor, 
                order=order, 
                amount=amount,
                checksum=checksum)

            order.order_placed = True
            order.save()

            received_data['message'] = "Checksum Matched"
            return JsonResponse({'response': received_data})
        else:
            received_data['message'] = "Checksum Mismatched"
            print('order was not successful because' + response_dict['RESPMSG'])
            return JsonResponse({'response': response_dict})



        # checksum = ""
        # form = dict(request.POST)

        # response_dict = {}
        # order = None

        # for i in form.keys():
        #     response_dict[i] = form[i]
        #     if i == 'CHECKSUMHASH':
        #         checksum = form[i]

        #     if i == 'ORDER':
        #         order = Order.objects.get(id=int(form[i]))

        #     if i == 'CUST_ID':
        #         user = form[i]

        #     if i == 'VENDOR':
        #         vendor = form[i]

        #     if i == 'TXN_AMOUNT':
        #         amount = int(form[i])

        # # we will verify the payment using our merchant key and the checksum that we are getting from Paytm request.POST
        # verify = verify_checksum(response_dict, settings.PAYTM_SECRET_KEY, checksum)

        # if verify:
        #     if response_dict['RESPCODE'] == '01':
        #         print('order successful')
                
                
        #     else:
        #         print('order was not successful because' + response_dict['RESPMSG'])
        #         return JsonResponse({'response': response_dict})




