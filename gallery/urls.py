from django.urls import path

from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('artist/list/', views.ArtistListView.as_view(), name='artist-list'),
    path('artist/search/', views.ArtistSearchView.as_view(), name='artist-search'),
    path('artwork/list/', views.ArtworkListView.as_view(), name='artwork-list'),
    path('artwork/search/', views.ArtworkSearchView.as_view(), name='artwork-search'),
    path('artwork/create/', views.ArtworkCreateView.as_view(), name='artwork-create'),
    path('exhibition/create/', views.ExhibitionCreateView.as_view(),
         name='exhibition-create'),
]
