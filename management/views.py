import csv

from django.db.models import Avg, Count, Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView

from account.models import Applyment, User
from core.mixins import ManagerOnlyMixin
from core.validators import ApproveRejectValidator
from gallery.models import Artist


class ApplymentManageView(ManagerOnlyMixin, View):
    '''
    작가등록신청관리 View

    Raises:
        GET:
            NOT is_authenticated:   로그인 페이지
            NOT is_manager:         401_UNAUTHORIZED
        POST:
            form invalid:           Form Error 출력

    Returns:
        GET:    작가등록신청관리 페이지
        POST:   작가등록신청 일괄처리 요청 후 작가등록신청관리 페이지
    '''

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
        Applyment.objects.filter(id__in=approve_list).update(
            is_approved=True, is_rejected=False)
        Applyment.objects.filter(id__in=reject_list).update(
            is_rejected=True, is_approved=False)
        User.objects.filter(
            applyment__pk__in=approve_list).update(is_artist=True)
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


class ApplymentSearchView(ManagerOnlyMixin, ListView):
    '''
    작가등록신청 검색 View

    Attrs:
        model:                  Applyment 모델
        context_object_name:    "applyments"
        template_name:          작가등록신청관리 템플릿

    Raises:
        NOT is_authenticated:   로그인 페이지
        NOT is_manager:         401_UNAUTHORIZED

    Returns:
        No Keyword:     비어있는 목록 출력
        Option:
            name, email:                keyword를 포함하는 검색 결과
            gender, birth_date, phone:  keyword와 일치하는 검색 결과
    '''
    model = Applyment
    context_object_name = 'applyments'
    template_name = "management/applyment.html"

    def get_queryset(self):
        '''
        작가등록신청 검색 결과 queryset method

        Returns:
            No Keyword:     비어있는 목록 출력
            Option:
                name, email:                keyword를 포함하는 검색 결과
                gender, birth_date, phone:  keyword와 일치하는 검색 결과
        '''
        option = self.request.GET.get("search-option")
        keyword = self.request.GET.get("search-keyword")
        queryset = []
        if not keyword:
            return queryset
        if option in ['name', 'email']:
            queryset = Applyment.objects.filter(
                **{f'{option}__icontains': keyword}).order_by('-created_at')
        elif option in ['gender', 'birth_date', 'phone']:
            queryset = Applyment.objects.filter(
                **{option: keyword}).order_by('-created_at')
        return queryset


class ApplymentDownloadView(ManagerOnlyMixin, View):
    '''
    작가등록신청내역 CSV 다운로드 View

    Raises:
        NOT is_authenticated:   로그인 페이지
        NOT is_manager:         401_UNAUTHORIZED

    Returns:
        작가등록신청내역 CSV 파일
    '''

    def get(self, request):
        applyments = Applyment.objects.all().order_by('-created_at')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="applyments.csv"'
        writer = csv.writer(response)
        writer.writerow(['이름', '성별', '생년월일', '이메일',
                        '연락처', '신청 일시', '승인', '반려'])
        for applyment in applyments:
            gender_value = '남성' if applyment.gender == 'm' else '여성'
            is_approved_value = 'v' if applyment.is_approved else ''
            is_rejected_value = 'v' if applyment.is_rejected else ''
            writer.writerow([applyment.name, gender_value, applyment.birth_date, applyment.email,
                            applyment.phone, applyment.created_at, is_approved_value, is_rejected_value])
        return response


class ArtistStatisticsView(ManagerOnlyMixin, ListView):
    '''
    작가 통계 View

    Attrs:
        model:                  작가 모델
        context_object_name:    "artists"
        template_name:          작가 통계 템플릿

    Raises:
        NOT is_authenticated:   로그인 페이지
        NOT is_manager:         401_UNAUTHORIZED

    Returns:
        작가 통계 페이지
    '''
    model = Artist
    context_object_name = 'artists'
    template_name = "management/statistics.html"

    def get_queryset(self):
        '''
        작가 통계 queryset method

        Returns:
            작가 별 작품수, 100호 이하 작품수, 작품 평균가격 결과
        '''
        queryset = Artist.objects.annotate(
            artwork_count=Count('artworks'),
            artwork_count_lte_size_100=Count(
                'artworks', filter=Q(artworks__size__lte=100)),
            artwork_avg_price=Avg('artworks__price')
        )
        return queryset
