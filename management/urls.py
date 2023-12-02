from django.urls import path

from . import views

app_name = 'management'

urlpatterns = [
    path('management/apply/', views.ApplymentManageView.as_view(), name='apply'),
]

