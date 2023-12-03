# Django-gallery

## Environment

- Python 3.11.6
- Django 4.2.7

## Installation

### Download

```bash
$ git clone https://github.com/jjiisub/Django-gallery.git
$ cd Django-gallery
$ pip install -r requirements.txt
```

### Database Setup

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

### Backend

```bash
$ python manage.py runserver
```

## Features

### Endpoints

|      App      |        Path        | Description |
| :-----------: | :----------------: | :---------: |
|  `account/`   |      signup/       |             |
|               |       login/       |             |
|               |      logout/       |             |
|               |       apply/       |             |
|               |     dashboard/     |             |
|  `gallery/`   |    artist/list/    |             |
|               |   artwork/list/    |             |
|               |  artwork/create/   |             |
|               | exhibition/create/ |             |
| `management/` |       apply/       |             |

### Demo

ScreenShots

## Troubleshootings

> ### 성능 최적화

#### 작가등록신청 관리

하나의 쿼리로 처리 가능하도록 구현

```python
## management/views.py

class ApplymentManageView(ManagerOnlyMixin, View):
    ...
    def post(self, request):
        ...
        Applyment.objects.filter(id__in=approve_list).update(is_approved=True, is_rejected=False)
        Applyment.objects.filter(id__in=reject_list).update(is_rejected=True, is_approved=False)
        User.objects.filter(applyment__pk__in=approve_list).update(is_artist=True)
        ...
```

> ### 기능 구현

#### Form Field Validation

작가등록신청(생년월일, 연락처), 작품등록(가격, 호수), 전시등록(시작일, 종료일) 페이지의 필드 오류를 처리하기 위해 각 필드 별 validator를 구현했습니다. DB 저장 이전에 validation 체크를 진행할 수 있도록 각 model 선언 시에 field validator를 추가했습니다. 이메일 필드는 models.EmailField를 이용해서 내장 email validation을 적용했습니다.

중복해서 사용되는 validator의 코드 재사용성을 높이기 위해 core 앱 내부에 validators.py를 만들어 validator들을 모두 저장했습니다.

```python
## core/validators.py
def DateValidator(value):
    pattern = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$')
    if not bool(pattern.match(str(value))):
        raise ValidationError("YYYY-MM-DD 형식의 날짜를 입력하세요.")

def PhoneValidator(value):
...

def ArtworkPriceValidator(value):
...

def ArtworkSizeValidator(value):
...


## account/models.py
from core.validators import DateValidator, PhoneValidator

class Applyment(models.Model):
    birth_date = models.DateField(validators=[DateValidator])
    phone = models.CharField(validators=[PhoneValidator], max_length=15)
    ...


## gallery/models.py
from core.validators import ArtworkPriceValidator, ArtworkSizeValidator

class Artwork(models.Model):
    price = models.IntegerField(validators=[ArtworkPriceValidator])
    size = models.IntegerField(validators=[ArtworkSizeValidator])
    ...
```

#### 작가 등록신청 관리 validation

작가 등록신청을 하면 Applyment 객체가 생성됩니다. 승인 여부는 is_approved와 is_rejected 필드를 이용해서 처리됩니다. 이때 작가 등록신청 관리 페이지에서 승인과 반려를 모두 체크해서 요청할 경우, ApproveRejectValidator를 이용하여 확인하고 에러를 발생하도록 구현했습니다.

```python
## core/validators.py
def ApproveRejectValidator(approve_list, reject_list):
    if set(approve_list) & set(reject_list):
        raise ValidationError("승인과 반려를 동시에 체크할 수 없습니다.")


## management/views.py
from core.validators import ApproveRejectValidator

class ApplymentManageView(ManagerOnlyMixin, View):
    ...
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
        ...
```

#### 전시 등록 페이지 작품 목록 form

전시 등록 페이지로 GET 요청 시 form에 request.user를 입력받아 해당 작가의 작품만 출력되도록 구현했습니다. 이후 선택된 작품 목록을 getlist로 가져와 해당 작품들을 Exhibition 객체에 저장했습니다.

```python
## gallery/forms.py
class ExhibitionCreateForm(forms.ModelForm):
    artworks = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(
            attrs={'class':'form-check-input me-1'}
        )
    )

    def __init__(self, user, *args, **kwargs):
        super(ExhibitionCreateForm, self).__init__(*args, **kwargs)
        self.fields['artworks'].queryset = Artwork.objects.filter(artist=user.artist)
    ...

## gallery/views.py
class ExhibitionCreateView(ArtistRequiredMixin, View):
    def get(self, request):
        form = ExhibitionCreateForm(request.user)
        context = {
            'form': form,
        }
        return render(request, 'gallery/exhibition_create.html', context)

    def post(self, request):
        form = ExhibitionCreateForm(request.user, request.POST)
        if form.is_valid():
            exhibition = form.save(commit=False)
            exhibition.artist = request.user.artist
            exhibition.save()
            artworks = request.POST.getlist('artworks')
            exhibition.artworks.set(artworks)
        ...
```

> ### Authorization

#### 유저 권한 설정 mixin

AccessMixin을 상속받아 ArtistRequiredMixin과 ManagerOnlyMixin을 구현했습니다. Custom Mixin을 상속받아 각 view class 내부에서 권한확인 코드의 반복을 줄였습니다.

```python
## core/mixins.py
class ArtistRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')
        elif not request.user.is_artist:
            return redirect('gallery:artist-list')
        ...


class ManagerOnlyMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')
        elif not request.user.is_manager:
            return redirect('gallery:artist-list')
        ...


## gallery/views.py
class ExhibitionCreateView(ArtistRequiredMixin, View):
    ...


## management/views.py
class ApplymentManageView(ManagerOnlyMixin, View):
    ...
```

> ### Errors

#### 400_BAD_REQUEST

#### 401_NOT_AUTHORIZED

#### 404_NOT_FOUND
