from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
import datetime

from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import Restaurant, MenuCategory, Menu, RestaurantType, similarityCalculation
from .serializers import RestaurantSerializer, MenuCategorySerializer, MenuSerializer, \
    MenuCategoryListBasedOnRestaurant, RestaurantCategorySerializer

from algorithm.cosine_similarity import descriptionCosineSimilarity


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


class RestaurantCategoryAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RestaurantCategorySerializer

    def get_queryset(self):
        request = self.request
        qs = RestaurantType.objects.all()
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


class MenuCategoryListBasedOnRestaurantAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MenuCategoryListBasedOnRestaurant

    def get_queryset(self, *args, **kwargs):
        restaurant = self.kwargs.get("id", None)
        if restaurant is None:
            return MenuCategory.objects.none()
        return MenuCategory.objects.filter(restaurant_id=restaurant)


class RestaurantBasedOnTypesAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantSerializer

    def get_queryset(self, *args, **kwargs):
        restaurantType_id = self.kwargs.get("id", None)
        if restaurantType_id is None:
            return Restaurant.objects.none()
        return Restaurant.objects.filter(restaurantType__id=restaurantType_id)


class CheckSimilarityOfRestaurants(APIView):
    permissions_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            restaurantA = Restaurant.objects.all()
            for rA in restaurantA:
                for rB in restaurantA:
                    similarityCalculationObjectsAwithB = similarityCalculation.objects.filter(restaurantA=rA,
                                                                                              restaurantB=rB)
                    similarityCalculationObjectsBwithA = similarityCalculation.objects.filter(restaurantA=rB,
                                                                                              restaurantB=rA)
                    if similarityCalculationObjectsAwithB.exists():
                        continue
                    elif similarityCalculationObjectsBwithA.exists():
                        continue
                    elif rA.id == rB.id:
                        continue
                    else:
                        similarityPercentage = descriptionCosineSimilarity(rA.description, rB.description)
                        if similarityPercentage >= 0.15:
                            similarity = similarityCalculation.objects.create(restaurantA=rA, restaurantB=rB,
                                                                              similarityPercent=float(
                                                                                  similarityPercentage))
                            similarity.save()
                        else:
                            print("Restaurant are not similar.")
            return Response({"message": "done", "status": status.HTTP_200_OK})
        except Exception as e:
            print(e)
            return Response({"message": "creation failed", "status": status.HTTP_417_EXPECTATION_FAILED})

    def patch(self, request, *args, **kwargs):
        try:
            similarityCalculationObjects = similarityCalculation.objects.all()
            for sc in similarityCalculationObjects:
                rA = sc.restaurantA
                rB = sc.restaurantB
                similarityPercentage = descriptionCosineSimilarity(rA.description, rB.description)
                if similarityPercentage >= 0.15:
                    sc.similarityPercent = similarityPercentage
                    sc.save()
                else:
                    sc.delete()
                    print("Restaurant are not similar.")
            return Response({"message": "done", "status": status.HTTP_200_OK})
        except Exception as e:
            print(e)
            return Response({"message": "update failed", "status": status.HTTP_417_EXPECTATION_FAILED})


class GetSimilarRestaurants(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RestaurantSerializer

    def get_queryset(self, *args, **kwargs):
        restaurantId = self.kwargs.get("id", None)
        if restaurantId is None:
            return Restaurant.objects.none()
        similarities = similarityCalculation.objects.filter(
            Q(restaurantA__id__iexact=restaurantId) | Q(restaurantB__id__iexact=restaurantId)).order_by('-similarityPercent')

        id_set = []
        for s in similarities:
            if s.restaurantA.id == restaurantId:
                id_set.append(s.restaurantB.id)
            elif s.restaurantB.id == restaurantId:
                id_set.append(s.restaurantA.id)
        return Restaurant.objects.filter(id__in=id_set)
