from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from .models import Restaurant
from .serializers import RestaurantSerializer


# Create your views here.


class RestaurantViewAPI(ListAPIView):
    permission_classes = []
    authentication_classes = []
    # queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        qs = Restaurant.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(name__icontains=query)
        return qs


class CreateRestaurantAPI(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class DetailRestaurantAPI(RetrieveAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    # lookup_field = 'id'

    def get_object(self, *args, **kwargs):
        kwargs = self.kwargs
        kw_id = kwargs.get('id')
        return Restaurant.objects.get(id=kw_id)


class UpdateRestaurantAPI(UpdateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'id'



class DeleteRestaurantAPI(DestroyAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'id'


