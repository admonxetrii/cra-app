from rest_framework import serializers
from api.models import Restaurant, MenuCategory, Menu, RestaurantType, RestaurantTable, RestaurantFloorLevel, \
    TableReservationDates, similarityCalculation, IsFavourite
from accounts.api.serializers import UserProfileSerializer


class RestaurantCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantType
        fields = [
            'id',
            'name',
            'icon',
        ]

    def validate(self, data):
        name = data.get("name", None)
        if name == "":
            name = None
        icon = data.get("icon", None)
        if name is None and icon is None:
            raise serializers.ValidationError("Name or image is required.")
        return data


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'icon',
            'image',
            'address',
            'description',
            'isOpenNow',
            'openingTime',
            'closingTime',
            'rating',
            'isClosedTemporarily',
            'addedDate',
            'modifiedDate',
        ]
        read_only_fields = ['modifiedBy']

    def validate(self, data):
        name = data.get("name", None)
        if name == "":
            name = None
        image = data.get("image", None)
        if name is None and image is None:
            raise serializers.ValidationError("Name or image is required.")
        return data


class SimilaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = similarityCalculation
        fields = [
            'similarityPercent',
            'restaurantA',
            'restaurantB'
        ]


class MenuCategorySerializer(serializers.ModelSerializer):
    # restaurant = RestaurantSerializer()

    class Meta:
        model = MenuCategory
        fields = [
            'id',
            'title',
            'restaurant'
        ]


class RestaurantFloorLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantFloorLevel
        fields = [
            'id',
            'floorName',
            'restaurant'
        ]


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            'id',
            'title',
            'price',
        ]


class TableReservationDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableReservationDates
        fields = [
            'id',
            'date',
            'user'
        ]


class TableSerializer(serializers.ModelSerializer):
    reservation_dates = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RestaurantTable
        fields = [
            'id',
            'tableName',
            'seatCapacity',
            'isOccupied',
            'occHrs',
            'occMin',
            'merged',
            'reservation_dates'
        ]
        read_only_fields = ['reservation_dates']

    def get_reservation_dates(self, obj):
        qs = obj.table.all()
        return TableReservationDateSerializer(qs, many=True).data


class IsFavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsFavourite
        fields = [
            'is_favourite'
        ]


class MenuCategoryListBasedOnRestaurant(serializers.ModelSerializer):
    menus = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MenuCategory
        fields = [
            'id',
            'title',
            'icon',
            'menus',
        ]
        read_only_fields = ['menus']

    def get_menus(self, obj):
        qs = obj.category.all()
        return MenuSerializer(qs, many=True).data


class FloorLevelListBasedOnRestaurant(serializers.ModelSerializer):
    tables = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RestaurantFloorLevel
        fields = [
            'id',
            'floorName',
            'tables',
        ]
        read_only_fields = ['tables']

    def get_tables(self, obj):
        qs = obj.floorLevel.all()
        return TableSerializer(qs, many=True).data


class ReservedTablesFloorLevelSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()

    class Meta:
        model = RestaurantFloorLevel
        fields = [
            'id',
            'floorName',
            'restaurant'
        ]


class ReservedTablesSerializer(serializers.ModelSerializer):
    floorLevel = ReservedTablesFloorLevelSerializer()

    class Meta:
        model = RestaurantTable
        fields = [
            'id',
            'tableName',
            'floorLevel'
        ]


class ReservationsByUserSerializer(serializers.ModelSerializer):
    table = ReservedTablesSerializer()

    class Meta:
        model = TableReservationDates
        fields = [
            'id',
            'date',
            'groupSize',
            'confirmation',
            'table',
        ]
