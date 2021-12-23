from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile');
    phonenumber = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    add1 = models.CharField(max_length=200, null=True, blank=True)
    add2 = models.CharField(max_length=200, null=True, blank=True)


class Profilepic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='User/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Profilepic.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(Profilepic, self).save(*args, **kwargs)
