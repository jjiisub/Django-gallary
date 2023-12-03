from django.urls import path

from . import views

app_name = 'management'

urlpatterns = [
    path('apply/', views.ApplymentManageView.as_view(), name='apply'),
    path('apply/search/', views.ApplymentSearchView.as_view(), name='apply-search'),
    path('apply/download/', views.ApplymentDownloadView.as_view(), name='apply-download'),
    path('statistics/', views.ArtistStatisticsView.as_view(), name='statistics'),
]

