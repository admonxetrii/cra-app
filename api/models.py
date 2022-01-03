from django.conf import settings
from django.db import models


# my custom methods


# Create your models here.
class RestaurantType(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    icon = models.ImageField(upload_to="uploads/restaurants/typeImages", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "RESTAURANT_TYPE"


class Restaurant(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    icon = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to="uploads/restaurants", null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    isOpenNow = models.BooleanField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    isClosedTemporarily = models.BooleanField(null=True, blank=True)
    addedDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modifiedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Restaurant.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except Exception as e:
            print(e)  # when new photo then we do nothing, normal case
        super(Restaurant, self).save(*args, **kwargs)

    class Meta:
        db_table = "RESTAURANT"


class RestaurantTypeOfRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    restaurantType = models.ForeignKey(RestaurantType, on_delete=models.CASCADE)

    def __str__(self):
        return self.restaurant.name + " " + self.restaurantType.name

    class Meta:
        db_table = "RESTAURANT_TYPE_OF_RESTAURANT"


class RestaurantFeaturedMenu(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "RESTAURANT_FEATURED_MENU"


class RestaurantFeaturedMenuForRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    restaurantFeaturedMenu = models.ForeignKey(RestaurantFeaturedMenu, on_delete=models.CASCADE)

    def __str__(self):
        return self.restaurantFeaturedMenu.name + "'s " + self.restaurant.name

    class Meta:
        db_table = "RESTAURANT_FEATURED_MENU_FOR_RESTAURANT"


class MenuCategory(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    icon = models.ImageField(upload_to="uploads/category", null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.restaurant.name + "'s " + self.title

    def delete(self, *args, **kwargs):
        self.icon.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Restaurant.objects.get(id=self.id)
            if this.image != self.icon:
                this.image.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(MenuCategory, self).save(*args, **kwargs)

    class Meta:
        db_table = "MENU_CATEGORY"


class Menu(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    icon = models.ImageField(upload_to="uploads/menu", null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.category.restaurant.name + "'s " + self.title

    def delete(self, *args, **kwargs):
        self.icon.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Restaurant.objects.get(id=self.id)
            if this.image != self.icon:
                this.image.delete(save=False)
        except Exception as e:
            print(e)  # when new photo then we do nothing, normal case
        super(Menu, self).save(*args, **kwargs)

    class Meta:
        db_table = "MENU"
