from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Restaurant
from .serializers import RestaurantSerializer


# Create your views here.


class RestaurantViewAPI(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, format=None):
        qs = Restaurant.objects.all()
        serializer = RestaurantSerializer(qs, many=True)
        return Response(serializer.data)
