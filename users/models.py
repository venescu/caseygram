from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from notifications.signals import notify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.CharField(max_length=150, blank=True)
    # bio is a field in this Post model. it specifies a class attribute Charfield and represents a database column
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)

    #     img = Image.open(self.image.path)  # will open the image path of the current image

    #     if img.height > 250 or img.width > 300:
    #         output_size = (250, 250)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    being_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='being_followeds')
    date_followed = models.DateTimeField(default=timezone.now)

    # def __str__(self):
    #     return f'{self.follower.username, self.being_followed.username} follower-> followee'

    def save(self, *args, **kwargs):
        super(Follower, self).save(*args, **kwargs)
        notify.send(self.follower, recipient=self.being_followed, verb='followed you!', description='follow', target=self)
