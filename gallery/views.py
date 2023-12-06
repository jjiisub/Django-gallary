from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.list import ListView

from core.mixins import ArtistRequiredMixin

from .forms import ArtworkCreateForm, ExhibitionCreateForm
from .models import Artist, Artwork


class IndexView(View):
    '''
    메인페이지 View

    Returns:
        메인페이지
    '''

    def get(self, request):
        return render(request, "gallery/index.html")


class ArtistListView(ListView):
    '''
    작가 목록조회 View

    Attrs:
        model:                  작가 모델
        ordering:               최근 등록된 순서
        context_object_name:    "artists"

    Returns:
        작가 목록조회 페이지
    '''
    model = Artist
    ordering = '-created_at'
    context_object_name = 'artists'


class ArtistSearchView(ListView):
    '''
    작가 검색 View

    Attrs:
        model:                  작가 모델
        context_object_name:    "artists"
        template_name:          작가 목록조회 템플릿

    Returns:
        No Keyword:     비어있는 목록 출력
        Option:
            name, email:                keyword를 포함하는 검색 결과
            gender, birth_date, phone:  keyword와 일치하는 검색 결과
    '''
    model = Artist
    context_object_name = 'artists'
    template_name = "gallery/artist_list.html"

    def get_queryset(self):
        '''
        작가 검색 결과 queryset method

        Returns:
            No Keyword:     비어있는 목록 출력
            Option:
                name, email:                keyword를 포함하는 검색 결과
                gender, birth_date, phone:  keyword와 일치하는 검색 결과
        '''
        option = self.request.GET.get("search-option")
        keyword = self.request.GET.get("search-keyword")
        queryset = []
        if not keyword:
            return queryset
        if option in ['name', 'email']:
            queryset = Artist.objects.filter(
                **{f'{option}__icontains': keyword}).order_by('-created_at')
        elif option in ['gender', 'birth_date', 'phone']:
            queryset = Artist.objects.filter(
                **{option: keyword}).order_by('-created_at')
        return queryset


class ArtworkListView(ListView):
    '''
    작품 목록조회 View

    Attrs:
        model:                  작품 모델
        ordering:               최근 등록된 순서
        context_object_name:    "artworks"

    Returns:
        작품 목록조회 페이지
    '''
    model = Artwork
    ordering = '-created_at'
    context_object_name = 'artworks'


class ArtworkSearchView(ListView):
    '''
    작가 검색 View

    Attrs:
        model:                  작품 모델
        context_object_name:    "artworks"
        template_name:          작품 목록조회 템플릿

    Returns:
        No Keyword:         비어있는 목록 출력
        Option:
            title:          keyword를 포함하는 검색 결과
            price, size:    keyword 이상 또는 이하의 결과
    '''
    model = Artwork
    context_object_name = 'artworks'
    template_name = "gallery/artwork_list.html"

    def get_queryset(self):
        '''
        작품 검색 결과 queryset method

        Returns:
            No Keyword:         비어있는 목록 출력
            Option:
                title:          keyword를 포함하는 검색 결과
                price, size:    keyword 이상 또는 이하의 결과
        '''
        option = self.request.GET.get("search-option")
        keyword = self.request.GET.get("search-keyword")
        queryset = []
        if option == 'title':
            queryset = Artwork.objects.filter(
                title__icontains=keyword).order_by('-created_at')
        elif option == 'price' or option == 'size':
            comp = self.request.GET.get("search-option-compare")
            option_compare = '__gte' if comp == "more" else '__lte'
            try:
                queryset = Artwork.objects.filter(
                    **{f'{option}{option_compare}': keyword}).order_by('-created_at')
            except:
                pass
        return queryset


class ArtworkCreateView(ArtistRequiredMixin, View):
    '''
    작품 등록 View

    Raises:
        GET:
            NOT is_authenticated:   로그인 페이지
            NOT is_artist:          401_UNAUTHORIZED
        POST:
            form invalid:           Form Error 출력

    Returns:
        GET:    작품 등록 페이지
        POST:   작품 등록 요청 후 작가 대시보드
    '''

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
            return redirect("account:dashboard")
        else:
            context = {
                'form': form,
            }
            return render(request, "gallery/artwork_create.html", context)


class ExhibitionCreateView(ArtistRequiredMixin, View):
    '''
    전시 등록 View

    Raises:
        GET:
            NOT is_authenticated:   로그인 페이지
            NOT is_artist:          401_UNAUTHORIZED
        POST:
            form invalid:           Form Error 출력

    Returns:
        GET:    전시 등록 페이지
        POST:   전시 등록 요청 후 작가 대시보드
    '''

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
            return redirect("account:dashboard")
        else:
            context = {
                'form': form,
            }
            return render(request, "gallery/exhibition_create.html", context)
