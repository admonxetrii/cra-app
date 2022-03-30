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
    RestaurantTable, Favourites, IsFavourite
from .serializers import RestaurantSerializer, MenuCategorySerializer, MenuSerializer, \
    MenuCategoryListBasedOnRestaurant, RestaurantCategorySerializer, FloorLevelListBasedOnRestaurant, \
    TableReservationDates, ReservationsByUserSerializer, SimilaritySerializer, IsFavouriteSerializer

from algorithm.cosine_similarity import descriptionCosineSimilarity


# Create your views here.
class RestaurantAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        request = self.request
        qs = Restaurant.objects.all().order_by('?')[:10]
        query = request.GET.get('q')
        if query is not None:
            qs = Restaurant.objects.filter(name__icontains=query)
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


class GetSimilarityPercentageSerializer(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SimilaritySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["restaurant_id"] = self.kwargs["id"]

    def get_queryset(self, *args, **kwargs):
        restaurantId = self.kwargs.get("id", None)
        if restaurantId is None:
            return similarityCalculation.objects.none()
        similarities = similarityCalculation.objects.filter(
            Q(restaurantA__id__iexact=restaurantId) | Q(restaurantB__id__iexact=restaurantId)).order_by(
            '-similarityPercent')[:10]
        return similarities


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

        restaurants = []
        for s in similarities:
            if s.restaurantA.id == restaurantId:
                restaurants.extend(list(Restaurant.objects.filter(id=s.restaurantB.id)))
            elif s.restaurantB.id == restaurantId:
                restaurants.extend(list(Restaurant.objects.filter(id=s.restaurantA.id)))
        return restaurants


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


class FavouriteRestaurant(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantSerializer

    def get_queryset(self, *args, **kwargs):
        username = self.kwargs.get("username", None)
        if username is None:
            return Restaurant.objects.none()
        favourites = Favourites.objects.filter(user__username=username)

        restaurants = []
        for f in favourites:
            restaurants.extend(list(Restaurant.objects.filter(id=f.restaurant.id)))
        return restaurants


class EditFavourite(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantSerializer

    def post(self, request, *args, **kwargs):
        restaurant_id = request.data.get('restaurant')
        username = request.data.get('username')
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            user = CustomUser.objects.get(username=username)
            favourite = Favourites.objects.create(user=user, restaurant=restaurant)
            favourite.save()
            return Response({"message": "Favourite Added Successfully", "status": status.HTTP_200_OK})
        except Exception as e:
            print(e)
            return Response({"message": "No Favourites Created", "status": status.HTTP_400_BAD_REQUEST})

    def patch(self, request, *args, **kwargs):
        restaurant_id = request.data.get('restaurant')
        username = request.data.get('username')
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            user = CustomUser.objects.get(username=username)
            favourite = Favourites.objects.get(user=user, restaurant=restaurant)
            favourite.delete()
            return Response(
                {"message": "Favourite Removed Successfully", "deletedId": restaurant_id, "status": status.HTTP_200_OK})
        except Exception as e:
            print(e)
            return Response({"message": "No Favourite found", "status": status.HTTP_400_BAD_REQUEST})


class IsFavouriteAPI(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IsFavouriteSerializer

    def get_queryset(self, *args, **kwargs):
        username = self.request.GET.get('username')
        restaurant = self.request.GET.get('restaurant')
        print(username, restaurant)
        if restaurant is None:
            print("yah aayo")
            return Restaurant.objects.none()
        try:
            restaurantObj = Restaurant.objects.get(id=restaurant)
            favourites = Favourites.objects.filter(user__username=username, restaurant=restaurantObj)
            if favourites.exists():
                return IsFavourite.objects.filter(id=1)
            else:
                return IsFavourite.objects.filter(id=2)
        except Exception as e:
            print(e)
            return Response({"message": "Not Favourite ", "status": status.HTTP_400_BAD_REQUEST})
