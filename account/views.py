from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import ApplymentCreateForm, UserCreateForm
from .models import User


class UserCreateView(CreateView):
    template_name = "account/signup.html"
    form_class = UserCreateForm
    success_url = reverse_lazy("account:login")


class UserLoginView(LoginView):
    model = User
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_manager or self.request.user.is_artist:
            return reverse_lazy('account:dashboard')
        else:
            return reverse_lazy('gallery:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())


class UserLogoutView(LogoutView):
    model = User
    next_page = "gallery:index"


class ApplymentCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_artist:
            return render(request, "401.html")
        form = ApplymentCreateForm
        context = {
            'form': form,
        }
        return render(request, "account/applyment.html", context)

    def post(self, request):
        form = ApplymentCreateForm(request.POST)
        if form.is_valid():
            applyment = form.save(commit=False)
            applyment.user = request.user
            applyment.save()
            return redirect("gallery:index")
        else:
            context = {
                'form': form,
            }
            return render(request, "account/applyment.html", context)


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_artist:
            artist = request.user.artist
            artworks = artist.artworks.all()
            exhibitions = artist.exhibitions.all()
            context = {
                'artist': artist,
                'artworks': artworks,
                'exhibitions': exhibitions,
            }
            return render(request, "account/artist_dashboard.html", context)
        elif request.user.is_manager:
            return render(request, "account/manager_dashboard.html")
        else:
            redirect("account:apply")
