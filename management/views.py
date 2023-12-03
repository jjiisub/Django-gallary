from django.shortcuts import redirect, render
from django.db.models import Count, Avg, Q
from django.views.generic import ListView
from django.views import View

from core.validators import ApproveRejectValidator
from core.mixins import ManagerOnlyMixin
from account.models import Applyment, User
from gallery.models import Artist


class ApplymentManageView(ManagerOnlyMixin, View):
    def get(self, request):
        applyments = Applyment.objects.all().order_by('-created_at')
        context = {
            'applyments': applyments,
        }
        return render(request, "management/applyment.html", context)

    def post(self, request):
        approve_list = request.POST.getlist('approve')
        reject_list = request.POST.getlist('reject')
        try:
            ApproveRejectValidator(approve_list, reject_list)
        except:
            applyments = Applyment.objects.all().order_by('-created_at')
            context = {
                'applyments': applyments,
                'errors': '승인과 반려를 동시에 선택할 수 없습니다.',
            }
            return render(request, "management/applyment.html", context)
        Applyment.objects.filter(id__in=approve_list).update(is_approved=True, is_rejected=False)
        Applyment.objects.filter(id__in=reject_list).update(is_rejected=True, is_approved=False)
        User.objects.filter(applyment__pk__in=approve_list).update(is_artist=True)
        for pk in approve_list:
            applyment = Applyment.objects.get(pk=pk)
            new_artist = Artist.objects.create(
                user=applyment.user,
                name=applyment.name,
                gender=applyment.gender,
                birth_date=applyment.birth_date,
                email=applyment.email,
                phone=applyment.phone,
            )
            new_artist.save()
        return redirect("management:apply")


class ApplymentSearchView(ListView):
    model = Applyment
    context_object_name = 'applyments'
    template_name = "management/applyment.html"

    def get_queryset(self):
        option = self.request.GET.get("search-option")
        keyword = self.request.GET.get("search-keyword")
        queryset = []
        if not keyword:
            return queryset
        if option in ['name', 'email']:
            queryset = Artist.objects.filter(**{f'{option}__icontains': keyword})
        elif option in ['gender', 'birth_date', 'phone']:
            queryset = Artist.objects.filter(**{option: keyword})
        return queryset


class ArtistStatisticsView(ManagerOnlyMixin, ListView):
    model = Artist
    ordering = '-created_at'
    context_object_name = 'artists'
    template_name = "management/statistics.html"

    def get_queryset(self):
        queryset = Artist.objects.annotate(
            artwork_count=Count('artworks'),
            artwork_count_lte_size_100=Count('artworks', filter=Q(artworks__size__lte=100)),
            artwork_avg_price=Avg('artworks__price')
        )
        return queryset