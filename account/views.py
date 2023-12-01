from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import User
from .forms import UserCreateForm
# Create your views here.


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
            pass
        elif self.request.user.is_artist:
            pass
        else:
            return reverse_lazy('account:logout')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())

    # def form_invalid(self, form):
    #     # return render(self.request, self.template_name, {'form': form, 'error_message': 'Invalid username or password'})
    #     return HttpResponse("wrong id or password")


class UserLogoutView(LogoutView):
    model = User
    next_page = "account:login"