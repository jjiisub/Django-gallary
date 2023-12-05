from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import ApplymentCreateForm, UserCreateForm
from .models import User


class UserCreateView(CreateView):
    '''
    User 회원가입 View

    Attrs:
        template_name:  회원가입 템플릿
        form_class:     회원가입 form
        success_url:    로그인 페이지

    Returns:
        GET:    회원가입 페이지
        POST:   회원가입 요청 후 로그인 페이지
    '''
    template_name = "account/signup.html"
    form_class = UserCreateForm
    success_url = reverse_lazy("account:login")


class UserLoginView(LoginView):
    '''
    User 로그인 View

    Attrs:
        model:                          User 모델
        template_name:                  로그인 템플릿
        redirect_authenticated_user:    이미 로그인된 경우 메인페이지 이동

    Returns:
        GET:    로그인 페이지
        POST:   로그인 요청 결과
    '''
    model = User
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        '''
        로그인 성공 페이지 URL method

        Returns:
            is_manager:     관리자 대시보드
            is_artist:      작가 대시보드
            else:           메인페이지
        '''
        if self.request.user.is_manager or self.request.user.is_artist:
            return reverse_lazy('account:dashboard')
        else:
            return reverse_lazy('gallery:index')

    def form_valid(self, form):
        '''로그인 form 유효성 검사 method'''
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())


class UserLogoutView(LogoutView):
    '''
    User 로그아웃 View

    Attrs:
        model:      User 모델
        next_page:  메인페이지

    Returns:
        메인페이지
    '''
    model = User
    next_page = "gallery:index"


class ApplymentCreateView(LoginRequiredMixin, View):
    '''
    작가등록신청 View

    Raises:
        GET:
            NOT is_authenticated:   로그인 페이지
            is_artist:              401_UNAUTHORIZED
        POST:
            form invalid:           Form Error 출력
    Returns:
        GET:    작가등록신청 페이지
        POST:   작가등록신청 후 메인페이지
    '''

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
    '''
    대시보드 View

    Raises:
        NOT is_authenticated:   로그인 페이지

    Returns:
        GET:
            is_artist:          작가 대시보드
            is_manager:         관리자 대시보드
            is_authenticated:   작가등록신청 페이지
    '''

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
