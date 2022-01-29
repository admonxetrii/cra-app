from rest_framework import serializers
from api.models import Restaurant, MenuCategory, Menu, RestaurantType, RestaurantTable, RestaurantFloorLevel, \
    TableReservationDates


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
            'modifiedBy',
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
        ]


class TableSerializer(serializers.ModelSerializer):
    reservationDate = TableReservationDateSerializer()

    class Meta:
        model = RestaurantTable
        fields = [
            'id',
            'tableName',
            'seatCapacity',
            'isOccupied',
            'occHrs',
            'occMin',
            'reservationDate',
            'merged',
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
