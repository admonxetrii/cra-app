from rest_framework import serializers
from api.models import Restaurant, MenuCategory, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'icon',
            'image',
            'address',
            'isOpenNow',
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


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            'id',
            'title',
            'price',
            'category'
        ]
