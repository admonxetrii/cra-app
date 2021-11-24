from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins
from rest_framework.response import Response

from .models import Restaurant
from .serializers import RestaurantSerializer


# Create your views here.


class RestaurantViewAPI(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin, generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        request = self.request
        qs = Restaurant.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(name__icontains=query)
        return qs

    def get_object(self):
        request = self.request
        passed_id = request.GET.get('id', None)
        queryset = self.get_queryset()
        obj = None
        if passed_id is not None:
            obj = get_object_or_404(queryset, id=passed_id)
            self.check_object_permissions(request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        passed_id = request.GET.get('id', None)
        if passed_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# class CreateRestaurantAPI(CreateAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer

# def perform_create(self, serializer):
#     serializer.save(user=self.request.user)

#
# class DetailRestaurantAPI(RetrieveAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer
#     # lookup_field = 'id'
#
#     def get_object(self, *args, **kwargs):
#         kwargs = self.kwargs
#         kw_id = kwargs.get('id')
#         return Restaurant.objects.get(id=kw_id)
#
#
# class UpdateRestaurantAPI(UpdateAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer
#     lookup_field = 'id'
#
#
#
# class DeleteRestaurantAPI(DestroyAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer
#     lookup_field = 'id'
#
