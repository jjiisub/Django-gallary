from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect, render


class ArtistRequiredMixin(AccessMixin):
    '''
    is_artist 권한 확인 Mixin

    Returns:
        NOT is_authenticated:   로그인 페이지
        NOT is_artist:          401_UNAUTHORIZED
    '''

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')
        elif not request.user.is_artist:
            return render(request, "401.html")
        else:
            return super().dispatch(request, *args, **kwargs)


class ManagerOnlyMixin(AccessMixin):
    '''
    is_manager 권한 확인 Mixin

    Raises:
        NOT is_authenticated:   로그인 페이지
        NOT is_manager:          401_UNAUTHORIZED
    '''

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')
        elif not request.user.is_manager:
            return render(request, "401.html")
        else:
            return super().dispatch(request, *args, **kwargs)
