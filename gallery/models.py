from django.db import models

from account.models import User
from .validators import ArtworkPriceValidator, ArtworkSizeValidator


class Artist(models.Model):
    GENDER_CHOICE = [
        ('m', '남자'),
        ('f', '여자'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=5, choices=GENDER_CHOICE)
    birth_date = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Artwork(models.Model):
    title = models.CharField(max_length=64)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artworks')
    price = models.IntegerField(validators=[ArtworkPriceValidator])
    size = models.IntegerField(validators=[ArtworkSizeValidator])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Exhibition(models.Model):
    title = models.CharField(max_length=64)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    artworks = models.ManyToManyField(Artwork, related_name='exhibitions', blank=True)

    def __str__(self):
        return self.title