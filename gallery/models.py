from django.db import models

from account.models import User


class Artist(models.Model):
    GENDER_CHOICE = [
        ('m', '남성'),
        ('f', '여성'),
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
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    price = models.IntegerField()
    size = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Exhibition(models.Model):
    title = models.CharField(max_length=64)
    start_date = models.DateField()
    end_date = models.DateField()
    artworks = models.ManyToManyField(Artwork, related_name='exhibitions')

    def __str__(self):
        return self.title