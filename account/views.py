from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views import View

from .models import User
from .forms import UserCreateForm, ApplymentCreateForm



class UserCreateView(CreateView):
    template_name = "account/signup.html"
    form_class = UserCreateForm
    success_url = reverse_lazy("account:login")


class UserLoginView(LoginView):
    model = User
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_manager:
            return reverse_lazy('gallery:artwork-list')
        elif self.request.user.is_artist:
            return reverse_lazy('gallery:artwork-list')
        else:
            return reverse_lazy('gallery:artwork-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())


class UserLogoutView(LogoutView):
    model = User
    next_page = "gallery:artwork-list"


class ApplymentCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_artist:
            return redirect("gallery:artwork-list")
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
            return redirect("gallery:artwork-list")
        else:
            context = {
            'form': form,
            }
            return render(request, "account/applyment.html", context)
