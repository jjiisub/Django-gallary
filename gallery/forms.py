from django import forms

from .models import Artwork, Exhibition


class ArtworkCreateForm(forms.ModelForm):
    '''
    작품 생성 form

    Fields:
        title:  작품 제목
        price:  작품 가격
        size:   작품 호수
    '''
    class Meta:
        model = Artwork
        fields = ['title', 'price', 'size']


class ExhibitionCreateForm(forms.ModelForm):
    '''
    전시 생성 form

    Fields:
        title:          전시 제목
        start_date:     전시 시작일
        end_date:       전시 종료일
        artworks:       전시 작품목록

    Returns:
        GET:    전체 작품 중 현재 user의 작품목록만 포함된 form
        POST:   artworks field가 None으로 초기화된 form
    '''
    start_date = forms.CharField(max_length=15)
    end_date = forms.CharField(max_length=15)
    artworks = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'form-check-input me-1'}
        )
    )

    def __init__(self, user, *args, **kwargs):
        '''
        전시 생성 form 초기화 method

        form 초기화 시 전체 작품들 중 현재 user의 작품목록만 출력

        Args:
            user:   현재 로그인된 유저
        '''
        super(ExhibitionCreateForm, self).__init__(*args, **kwargs)
        self.fields['artworks'].queryset = Artwork.objects.filter(
            artist=user.artist)

    class Meta:
        model = Exhibition
        fields = ['title', 'start_date', 'end_date', 'artworks']
