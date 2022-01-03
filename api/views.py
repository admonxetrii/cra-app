from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, permissions
from rest_framework.authentication import SessionAuthentication
import datetime

from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import Restaurant, MenuCategory, Menu
from .serializers import RestaurantSerializer, MenuCategorySerializer, MenuSerializer


# Create your views here.
class RestaurantAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        request = self.request
        qs = Restaurant.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(name__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(modifiedBy=self.request.user)


class RestaurantAPIDetailView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(modifiedBy=self.request.user, modifiedDate=datetime.datetime.now())


class MenuCategoryAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = MenuCategorySerializer

    def get_queryset(self):
        request = self.request
        qs = MenuCategory.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(title__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MenuCategoryDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    serializer_class = MenuCategorySerializer
    queryset = MenuCategory.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MenuAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        request = self.request
        qs = Menu.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(title__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MenuDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
