from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Artist, Artwork, Exhibition
# Create your views here.

class ArtistListView(ListView):
    model = Artist
    ordering = '-created_at'

class ArtworkListView(ListView):
    model = Artwork
    ordering = '-created_at'