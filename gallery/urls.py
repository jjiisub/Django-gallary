from django.urls import path

from . import views

app_name = 'gallery'

urlpatterns = [
    path('artist/list/', views.ArtistListView.as_view(), name='artist-list'),
    # path('artist/create/', views.UserCreateView.as_view(), name='signup'),
    path('artwork/list/', views.ArtworkListView.as_view(), name='artwork-list'),
    # path('artworks/create/', views.UserLoginView.as_view(), name='login'),
]

