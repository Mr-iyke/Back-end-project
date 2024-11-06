from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete = models.CASCADE)
    avatar =  models.ImageField(default = "avatar.jpg", upload_to = "avatars")
    gender =  models.CharField(max_length = 100)

    def __str__(self):
        return self.user.username
    
    def save(self, *arg, **kwarg):
        super().save(*arg, **kwarg)
        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)