from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Traveller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    permission = models.ManyToManyField(to=User, related_name='place_permission')
    picture = models.ImageField(blank=True, null=True)
    alt_email = models.EmailField(blank=True, null=True)
    street = models.CharField(blank=True, null=True, max_length=128)
    city = models.CharField(blank=True, null=True, max_length=128)
    zip = models.CharField(blank=True, null=True, max_length=32)
    country = models.CharField(blank=True, null=True, max_length=2)
    state = models.CharField(blank=True, null=True, max_length=2)
    vita = models.TextField(blank=True, null=True, max_length=1024)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Traveller.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.traveller.save()
