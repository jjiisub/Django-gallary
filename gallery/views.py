from django.views import View
from django.shortcuts import render, redirect
from django.views.generic.list import ListView

from .models import Artist, Artwork, Exhibition
from .mixins import ArtistRequiredMixin
from .forms import ArtworkCreateForm


class ArtistListView(ListView):
    model = Artist
    ordering = '-created_at'


class ArtworkListView(ListView):
    model = Artwork
    ordering = '-created_at'


class ArtworkCreateView(ArtistRequiredMixin, View):
    def get(self, request):
        form = ArtworkCreateForm
        context = {
            'form': form
        }
        return render(request, "gallery/artwork_create.html", context)
    
    def post(self, request):
        form = ArtworkCreateForm(request.POST)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.artist = request.user.artist
            artwork.save()
            return redirect("gallery:artwork-list")