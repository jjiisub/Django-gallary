from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.UserCreateView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('apply/', views.ApplymentCreateView.as_view(), name='apply'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]

