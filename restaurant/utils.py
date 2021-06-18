from geopy.geocoders import Nominatim
from geopy.distance import great_circle

from .models import Kitchen, KitchenAdress
from userinfo.models import UserAddress


def check_address_distance(user_pincode, kitchen_address):
    payload = []

    geolocator = Nominatim(user_agent = "geoapiExercises")
    location = geolocator.geocode(int(user_pincode))
    user_latitude = location.latitude
    user_longitude = location.longitude
 

    if user_pincode and kitchen_address:
        for address in kitchen_address:
            first = (float(user_latitude), float(user_longitude))
            second = (float(address.latitude), float(address.longitude))
            distance = int(great_circle(first, second).miles)

            if distance <=5:
                payload.append(address.kitchen.id)
            elif 5 < distance <=10:
                payload.append(address.kitchen.id)

    return payload



def takeaway_delivery_filter(serializer, user, query=None):
    user_address = UserAddress.objects.select_related('user').filter(user=user, active=True).first()
    kitchen_address = KitchenAdress.objects.all().select_related('kitchen')

    if user_address:
        payload = check_address_distance(user_address, kitchen_address)
        if query == 'takeaway':
            qs = Kitchen.objects.filter(pk__in = payload, takeaway=True)
        elif query == 'delivery':
            qs = Kitchen.objects.filter(pk__in = payload, delivery=True)
        elif query == 'both':
            qs = Kitchen.objects.filter(pk__in = payload, delivery=True, takeaway=True)
        if qs:
            kitchen = serializer(qs, many=True).data
            return kitchen
        return 'No kitchens available nearby.'
    return 'Kindly update your user address'