from django.db.models import Q
from django.shortcuts import get_object_or_404
from pip._internal.locations import user_site
from rest_framework import generics, mixins, permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from accounts.models import CustomUser
import datetime
import pytz

utc = pytz.timezone(zone="Asia/Kathmandu")

from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication, JWTAuthentication

from .models import Restaurant, MenuCategory, Menu, RestaurantType, similarityCalculation, RestaurantFloorLevel, \
    RestaurantTable, Favourites, IsFavourite, LikeTags
from .serializers import RestaurantSerializer, MenuCategorySerializer, MenuSerializer, \
    MenuCategoryListBasedOnRestaurant, RestaurantCategorySerializer, FloorLevelListBasedOnRestaurant, \
    TableReservationDates, ReservationsByUserSerializer, SimilaritySerializer, IsFavouriteSerializer, TagsSerializer

from algorithm.cosine_similarity import descriptionCosineSimilarity


# Create your views here.

class RestaurantCategoryAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RestaurantCategorySerializer

    def get_queryset(self):
        request = self.request
        qs = RestaurantType.objects.all()
        query = request.GET.get()
        if query is not None:
            qs = qs.filter(name__icontains=query)
        return qs


class RestaurantAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
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


class GetTagsAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TagsSerializer

    def get_queryset(self):
        qs = LikeTags.objects.all()
        return qs


class SaveUserTagsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            tags = request.data.get('tags')
            user_obj = CustomUser.objects.get(username=username)
            for tag in tags:
                tags_obj = LikeTags.objects.get(id=tag)
                user_obj.userTags.add(tags_obj)
                user_obj.has_tags = True
                user_obj.save()
            return Response({"message": "User Tags saved", "status": status.HTTP_200_OK})
        except Exception as e:
            print(e)
            return Response({"error": e, "status": status.HTTP_400_BAD_REQUEST})


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
    authentication_classes = [JWTAuthentication]
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
    authentication_classes = [JWTAuthentication]
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
    authentication_classes = [JWTAuthentication]
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
    authentication_classes = [JWTAuthentication]
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MenuCategoryListBasedOnRestaurant

    def get_queryset(self, *args, **kwargs):
        restaurant = self.kwargs.get("id", None)
        if restaurant is None:
            return MenuCategory.objects.none()
        return MenuCategory.objects.filter(restaurant_id=restaurant)


class RestaurantBasedOnTypesAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = RestaurantSerializer

    def get_queryset(self, *args, **kwargs):
        restaurantType_id = self.kwargs.get("id", None)
        if restaurantType_id is None:
            return Restaurant.objects.none()
        return Restaurant.objects.filter(restaurantType__id=restaurantType_id)


class CalculateRecommendation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            users = CustomUser.objects.all()
            print(users)
            return Response({"message": "creation failed"})
        except Exception as e:
            print(e)


class CheckSimilarityOfRestaurants(APIView):
    authentication_classes = [JWTAuthentication]
    permissions = [permissions.IsAuthenticated]

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
                        rATags_obj = rA.tags.all()
                        rBTags_obj = rB.tags.all()
                        rATags = []
                        rBTags = []
                        for rA_obj in rATags_obj:
                            rATags.append(rA_obj.tags)
                        for rB_obj in rBTags_obj:
                            rBTags.append(rB_obj.tags)

                        similarityPercentage = descriptionCosineSimilarity(rATags, rBTags)
                        if similarityPercentage >= 0.45:
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

                rATags_obj = rA.tags.all()
                rBTags_obj = rB.tags.all()
                rATags = []
                rBTags = []
                for rA_obj in rATags_obj:
                    rATags.append(rA_obj.tags)
                for rB_obj in rBTags_obj:
                    rBTags.append(rB_obj.tags)

                similarityPercentage = descriptionCosineSimilarity(rATags, rBTags)
                if similarityPercentage >= 0.45:
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
    authentication_classes = [JWTAuthentication]
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
    authentication_classes = [JWTAuthentication]
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
    authentication_classes = [JWTAuthentication]
    permissions = [permissions.IsAuthenticated]
    serializer_class = FloorLevelListBasedOnRestaurant

    def get_queryset(self, *args, **kwargs):
        restaurant = self.kwargs.get("id", None)
        if restaurant is None:
            return RestaurantFloorLevel.objects.none()
        return RestaurantFloorLevel.objects.filter(restaurant_id=restaurant)


class ReservedTableListByUserAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
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
            rsvp_date = r.startDate
            if r.confirmation:
                fourty_five_min = datetime.timedelta(minutes=45)
                print(current_datetime, fourty_five_min)
                rsvp_cancel_time = rsvp_date + fourty_five_min
                if current_datetime > rsvp_cancel_time:
                    r.cancelled = True
                    r.cancelled_reason = "USER_DIDNT_ARRIVED"
                    r.save()
                    print("User didn't arrived so cancelled")
            else:
                thirty_minute = datetime.timedelta(minutes=30)
                print(current_datetime, rsvp_date)
                rsvp_cancel_time = rsvp_date - thirty_minute
                if current_datetime > rsvp_cancel_time:
                    r.cancelled = True
                    r.cancelled_reason = "NOT_CONFIRMED_FROM_RESTAURANT"
                    r.save()
                    print("Not Confirmed")
        get_rsvp_obj_final = TableReservationDates.objects.filter(user__id=user, cancelled=False).order_by("startDate")
        return get_rsvp_obj_final


class ConfirmTableBookingAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, *arg, **kwargs):
        try:
            start = request.data.get('startDate')
            end = request.data.get('endDate')
            table_id = request.data.get('tableId')
            user = request.data.get('username')
            groupSize = request.data.get('groupSize')

            print(start, end, table_id, groupSize, user)

            try:
                user_obj = CustomUser.objects.get(username=user)
                table_obj = RestaurantTable.objects.get(id=table_id)
                startDate = datetime.datetime.fromtimestamp(start / 1000)
                endDate = datetime.datetime.fromtimestamp(end / 1000)

                print(startDate, endDate)

                if table_obj is not None:
                    reservationDate = TableReservationDates.objects.create(user=user_obj, table=table_obj,
                                                                           startDate=startDate, endDate=endDate,
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
                    rspv_obj.cancelled = True
                    rspv_obj.save()
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
    authentication_classes = [JWTAuthentication]
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
    authentication_classes = [JWTAuthentication]
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
    authentication_classes = [JWTAuthentication]
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
