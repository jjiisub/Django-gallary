from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.list import ListView

from .forms import ArtworkCreateForm, ExhibitionCreateForm
from core.mixins import ArtistRequiredMixin
from .models import Artist, Artwork, Exhibition


class ArtistListView(ListView):
    model = Artist
    ordering = '-created_at'
    context_object_name = 'artists'


class ArtworkListView(ListView):
    model = Artwork
    ordering = '-created_at'
    context_object_name = 'artworks'


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
        context = {
            'form': form,
        }
        return render(request, 'gallery/exhibition_create.html', context)

    def post(self, request):
        form = ExhibitionCreateForm(request.user, request.POST)
        if form.is_valid():
            exhibition = form.save(commit=False)
            exhibition.artist = request.user.artist
            exhibition.save()
            artworks = request.POST.getlist('artworks')
            exhibition.artworks.set(artworks)
            return redirect("gallery:exhibition-create")
        else:
            context = {
                'form': form,
            }
            return render(request, "gallery/exhibition_create.html", context)