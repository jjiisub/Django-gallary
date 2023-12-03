from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.list import ListView

from .forms import ArtworkCreateForm, ExhibitionCreateForm
from core.mixins import ArtistRequiredMixin
from .models import Artist, Artwork


class IndexView(View):
    def get(self, request):
        return render(request, "gallery/index.html")


class ArtistListView(ListView):
    model = Artist
    ordering = '-created_at'
    context_object_name = 'artists'

class ArtistSearchView(ListView):
    model = Artist
    context_object_name = 'artists'
    template_name = "gallery/artist_list.html"
    
    def get_queryset(self):
        option = self.request.GET.get("search-option")
        keyword = self.request.GET.get("search-keyword")
        queryset = []
        if not keyword:
            return queryset
        if option in ['name', 'email']:
            queryset = Artist.objects.filter(**{f'{option}__icontains': keyword})
        elif option in ['gender', 'birth_date', 'phone']:
            queryset = Artist.objects.filter(**{option: keyword})
        return queryset


class ArtworkListView(ListView):
    model = Artwork
    ordering = '-created_at'
    context_object_name = 'artworks'


class ArtworkSearchView(ListView):
    model = Artwork
    context_object_name = 'artworks'
    template_name = "gallery/artwork_list.html"
    
    def get_queryset(self):
        option = self.request.GET.get("search-option")
        keyword = self.request.GET.get("search-keyword")
        queryset = []
        if option=='title':
            queryset = Artwork.objects.filter(title__icontains=keyword)
        elif option=='price' or option=='size':
            comp = self.request.GET.get("search-option-compare")
            option_compare = '__gte' if comp=="more" else '__lte'
            try:
                queryset = Artwork.objects.filter(**{f'{option}{option_compare}': keyword})
            except:
                pass
        return queryset


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