from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers


class UnofficialRoute(object):
    def __init__(self, latitude, longitude, depth):
        self.latitude = latitude
        self.longitude = longitude
        self.depth = depth


route = UnofficialRoute(latitude="3.11112231", longitude="3.11121333", depth="4.6")


class UnofficialRouteSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    depth = serializers.FloatField()


@api_view(['GET'])
def unofficial_routes(request):
    latitude = request.GET.get('lon')
    longitude = request.GET.get('lat')

    route = UnofficialRoute(latitude=latitude, longitude=longitude, depth="2.0")
    serializer = UnofficialRouteSerializer(route)

    return Response(serializer.data)




