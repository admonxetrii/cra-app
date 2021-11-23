from django.conf import settings
from django.db import models


# my custom methods


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="uploads/restaurants", null=True, blank=True)
    addedDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modifiedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=30, null=True, blank=True)

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
        except:
            pass  # when new photo then we do nothing, normal case
        super(Restaurant, self).save(*args, **kwargs)

    class Meta:
        db_table = "RESTAURANT"
