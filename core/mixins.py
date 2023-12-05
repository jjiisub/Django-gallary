from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect, render


class ArtistRequiredMixin(AccessMixin):
    '''
    is_artist 권한 확인 Mixin

    Raises:
        로그인 페이지:         NOT is_authenticated
        401_UNAUTHORIZED:   NOT is_artist
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
        로그인 페이지:         NOT is_authenticated
        401_UNAUTHORIZED:   NOT is_manager
    '''

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')
        elif not request.user.is_manager:
            return render(request, "401.html")
        else:
            return super().dispatch(request, *args, **kwargs)
