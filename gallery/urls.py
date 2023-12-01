from django.urls import path

from . import views

app_name = 'gallery'

urlpatterns = [
    path('artist/list/', views.ArtistListView.as_view(), name='artist-list'),
    path('artwork/list/', views.ArtworkListView.as_view(), name='artwork-list'),
    path('artwork/create/', views.ArtworkCreateView.as_view(), name='artwork-create'),
    # path('exhibition/create/', views.UserCreateView.as_view(), name='signup'),
]

