from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from accounts.models import CustomUser
import datetime
import pytz

utc = pytz.timezone(zone="Asia/Kathmandu")

from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import Restaurant, MenuCategory, Menu, RestaurantType, similarityCalculation, RestaurantFloorLevel, \
    RestaurantTable
from .serializers import RestaurantSerializer, MenuCategorySerializer, MenuSerializer, \
    MenuCategoryListBasedOnRestaurant, RestaurantCategorySerializer, FloorLevelListBasedOnRestaurant, \
    TableReservationDates, ReservationsByUserSerializer

from algorithm.cosine_similarity import descriptionCosineSimilarity


# Create your views here.
class RestaurantAPIView(mixins.CreateModelMixin, generics.ListAPIView):
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
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
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
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = MenuCategoryListBasedOnRestaurant

    def get_queryset(self, *args, **kwargs):
        restaurant = self.kwargs.get("id", None)
        if restaurant is None:
            return MenuCategory.objects.none()
        return MenuCategory.objects.filter(restaurant_id=restaurant)


class RestaurantBasedOnTypesAPIView(generics.ListAPIView):
    serializer_class = RestaurantSerializer

    def get_queryset(self, *args, **kwargs):
        restaurantType_id = self.kwargs.get("id", None)
        if restaurantType_id is None:
            return Restaurant.objects.none()
        return Restaurant.objects.filter(restaurantType__id=restaurantType_id)


class CheckSimilarityOfRestaurants(APIView):
    permissions_classes = [permissions.IsAuthenticated]

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
            Q(restaurantA__id__iexact=restaurantId) | Q(restaurantB__id__iexact=restaurantId)).order_by(
            '-similarityPercent')[:10]

        id_set = []
        for s in similarities:
            if s.restaurantA.id == restaurantId:
                id_set.append(s.restaurantB.id)
            elif s.restaurantB.id == restaurantId:
                id_set.append(s.restaurantA.id)
        return Restaurant.objects.filter(id__in=id_set)


class TableListBasedOnRestaurantAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = FloorLevelListBasedOnRestaurant

    def get_queryset(self, *args, **kwargs):
        restaurant = self.kwargs.get("id", None)
        if restaurant is None:
            return RestaurantFloorLevel.objects.none()
        return RestaurantFloorLevel.objects.filter(restaurant_id=restaurant)


class ReservedTableListByUserAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReservationsByUserSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.kwargs.get("id", None)
        if user is None:
            return TableReservationDates.objects.none()

        now = datetime.datetime.now()
        current_datetime = utc.localize(now)
        rsvp_obj = TableReservationDates.objects.filter(user__id=user)
        for r in rsvp_obj:
            rsvp_date = r.date
            thirty_minute = datetime.timedelta(minutes=30)
            print(current_datetime, rsvp_date)
            rsvp_cancel_time = rsvp_date - thirty_minute
            if current_datetime > rsvp_cancel_time:
                r.delete()
                print("Time exceeded for ", r.date)
        get_rsvp_obj_final = TableReservationDates.objects.filter(user__id=user).order_by("date")
        return get_rsvp_obj_final


class ConfirmTableBookingAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, *arg, **kwargs):
        try:
            timestamp = request.data.get('date')
            table_id = request.data.get('tableId')
            user = request.data.get('username')
            groupSize = request.data.get('groupSize')

            print(timestamp, table_id, groupSize, user)

            try:
                user_obj = CustomUser.objects.get(username=user)
                table_obj = RestaurantTable.objects.get(id=table_id)
                date = datetime.datetime.fromtimestamp(timestamp / 1000)

                print(date)

                if table_obj is not None:
                    reservationDate = TableReservationDates.objects.create(user=user_obj, table=table_obj, date=date,
                                                                           groupSize=groupSize)
                    reservationDate.save()
                    return Response({"message": "Reservation Successful", "status": status.HTTP_200_OK})

            except Exception as e:
                print(e)
                return Response({"message": e, "status": status.HTTP_404_NOT_FOUND})

        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong!!", "status": status.HTTP_400_BAD_REQUEST})

    def patch(self, request, *args, **kwargs):
        try:
            reservation_id = request.data.get('reservationId')
            try:
                rspv_obj = TableReservationDates.objects.get(id=reservation_id)
                if rspv_obj is not None:
                    rspv_obj.delete()
                    return Response({"message": "Reservation has been cancelled.", "status": status.HTTP_200_OK,
                                     "deletedId": reservation_id})
                else:
                    return Response({"message": "No reservations Found", "status": status.HTTP_404_NOT_FOUND})

            except Exception as e:
                return Response({"message": "No reservations Found", "status": status.HTTP_404_NOT_FOUND})

        except Exception as e:
            print(e)
            return Response({"message": "No reservations Found", "status": status.HTTP_400_BAD_REQUEST})
