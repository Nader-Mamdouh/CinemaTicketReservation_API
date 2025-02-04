from django.db import models
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance, created, **kwargs):
    """Automatically create a token when a new user is created."""
    if created:
        Token.objects.create(user=instance)

# Create your models here.
# Geust - Movie - Reservation


class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=30)
    date = models.DateField()


class Guest(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=11)


class Reservation(models.Model):
    guest = models.ForeignKey(
        Guest, related_name="reservation", on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie, related_name="reservation", on_delete=models.CASCADE)
