from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from core.carrier.models import Order
from django.conf import settings
import googlemaps

gmaps = googlemaps.Client(key=settings.GMAPS_API_KEY)

class UpdateDriverPositionView(APIView):
    def patch(self, request, order_id):
        driver_position = request.data.get("driver_position")
        
        if not driver_position:
            return Response(
                {"detail": "Driver position is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = get_object_or_404(Order, id=order_id)

        if not order.id_delivery:
            return Response(
                {"detail": "Delivery not found for this order."},
                status=status.HTTP_404_NOT_FOUND
            )

        delivery = order.id_delivery
        delivery.driver_position = driver_position

        print(driver_position)
        latitude = driver_position.get("latitude")
        longitude = driver_position.get("longitude")
        print(latitude, longitude)
        print(order.id_delivery.address)
        lat_lng = gmaps.geocode(order.id_delivery.address)[0]["geometry"]["location"]
        print(lat_lng)

        delivery.distance = gmaps.distance_matrix(
            origins=[{"lat": latitude, "lng": longitude}],
            destinations=[lat_lng],
            mode="walking"
        )["rows"][0]["elements"][0]["distance"]["value"]

        delivery.save()


        return Response(
            {"detail": "Driver position updated successfully."},
            status=status.HTTP_200_OK
        )
