from django.contrib.auth import get_user_model

from django.db import models


User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile_images', default='blank-profile-photo.jpeg')
    location = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.user.username
