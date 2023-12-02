from django.views import View
from django.shortcuts import render, redirect
from django.views.generic.list import ListView

from .models import Artist, Artwork, Exhibition
from .mixins import ArtistRequiredMixin
from .forms import ArtworkCreateForm, ExhibitionCreateForm


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
            'form': form,
        }
        return render(request, "gallery/artwork_create.html", context)
    
    def post(self, request):
        form = ArtworkCreateForm(request.POST)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.artist = request.user.artist
            artwork.save()
            return redirect("gallery:artwork-list")
        else:
            context = {
                'form': form,
            }
            return render(request, "gallery/artwork_create.html", context)


class ExhibitionCreateView(ArtistRequiredMixin, View):
    def get(self, request):
        form = ExhibitionCreateForm(request.user)
        artist = request.user.artist
        artworks = artist.artworks.all()
        context = {
            'form': form,
            'artworks': artworks,
        }
        return render(request, 'gallery/exhibition_create.html', context)

    def post(self, request):
        form = ExhibitionCreateForm(request.user, request.POST)
        if form.is_valid():
            exhibition = form.save(commit=False)
            exhibition.artist = request.user.artist
            exhibition.save()
            return redirect("gallery:exhibition-create")
        else:
            artworks = request.user.artist.artworks.all()
            context = {
                'form': form,
                'artworks': artworks,
            }
            return render(request, "gallery/exhibition_create.html", context)