from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Follower
from homepage.models import Like, Comment, Post, PostImage
from directmessages.models import Message
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def create_follower(sender, instance, created, **kwargs):
    caseygramMainUser = User.objects.get(id=1)
    if created:
        Follower.objects.create(follower=instance, being_followed=instance)
        if not instance.pk == 1:
            Follower.objects.create(follower=instance, being_followed=caseygramMainUser)
            Follower.objects.create(follower=caseygramMainUser, being_followed=instance)
# creates a follower object so upon account creation, user is following my account and themselves.


@receiver(post_save, sender=User)
def create_objects(sender, instance, created, **kwargs):
    caseygramMainUser = User.objects.get(id=1)
    if created:
        Message.objects.create(sender=caseygramMainUser, receiver=instance, content='This is your inbox! Click me to view our conversation.')
        post = Post.objects.get(pk=1)
        Comment.objects.create(post=post, author=caseygramMainUser, content='Here is your first comment!')


@receiver(pre_delete, sender=Like)
@receiver(pre_delete, sender=Comment)
@receiver(pre_delete, sender=Message)
@receiver(pre_delete, sender=Follower)
def delete_notifications(sender, instance, **kwargs):
    qs = Notification.objects.get(target_object_id=instance.pk, target_content_type=ContentType.objects.get_for_model(instance))
    qs.delete()
