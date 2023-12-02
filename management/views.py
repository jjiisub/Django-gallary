from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views import View

from account.models import Applyment, User
from gallery.models import Artist

from .mixins import ManagerOnlyMixin
from .validators import ApproveRejectValidator


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