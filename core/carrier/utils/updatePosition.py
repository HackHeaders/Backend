from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from core.carrier.models import Order, AddressOrder
from django.conf import settings
import googlemaps


gmaps = googlemaps.Client(key=settings.GMAPS_API_KEY)


class UpdateDriverPositionView(APIView):
    """
    API endpoint to update the driver's position for a given order.
    """

    def patch(self, request, order_id: int) -> Response:
        """
        Updates the driver's position and calculates the distance to the delivery address.
        """
        # Validate driver position
        driver_position = request.data.get("driver_position")
        if not driver_position or not all(
            key in driver_position for key in ("latitude", "longitude")
        ):
            return Response(
                {"detail": "Driver position with 'latitude' and 'longitude' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the order and validate delivery existence
        order = get_object_or_404(Order, id=order_id)
        if not order.id_delivery:
            return Response(
                {"detail": "Delivery not found for this order."},
                status=status.HTTP_404_NOT_FOUND,
            )

        delivery = order.id_delivery
        delivery.driver_position = driver_position

        if not delivery.address:
            delivery_address_obj = AddressOrder.objects.filter(
                id_order=order, typeAddress=0
            ).first()
            if not delivery_address_obj:
                return Response(
                    {"detail": "Delivery address not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            delivery_address_complete = (
                f"{delivery_address_obj.street} {delivery_address_obj.number}, "
                f"{delivery_address_obj.neighborhood}, {delivery_address_obj.city}, "
                f"{delivery_address_obj.state}, {delivery_address_obj.cep}"
            )
        else:
            delivery_address_complete = delivery.address

        latitude = driver_position["latitude"]
        longitude = driver_position["longitude"]

        try:
            distance_all = gmaps.distance_matrix(
                origins=[{"lat": latitude, "lng": longitude}],
                destinations=[delivery_address_complete],
                mode="walking", # Change to "driving" if the driver is using a vehicle or "bicycling" if using a bike or transite for public transportation tem que alterar isso aqui pae
            )
            distance_element = distance_all["rows"][0]["elements"][0]

            if distance_element["status"] != "OK":
                return Response(
                    {"detail": f"Unable to calculate distance: {distance_element['status']}."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            delivery.distance = distance_element["distance"]["value"]
            delivery.address = delivery_address_complete
            delivery.save()

        except Exception as e:
            return Response(
                {"detail": f"An error occurred while calculating distance: {str(e)}."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"detail": "Driver position updated successfully."},
            status=status.HTTP_200_OK,
        )
