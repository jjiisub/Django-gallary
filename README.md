# Django-gallery

## Environment

---

- Python 3.11.6
- Django 4.2.7

## Installation

---

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

---

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

---

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

> ### Validation

#### Form Field Validation

#### - Form Field Validation

#### `Form Field Validation`

작가등록신청(생년월일, 연락처), 작품등록(가격, 호수), 전시등록(시작일, 종료일) 페이지의 필드 오류를 처리하기 위해 각 필드 별 validator를 구현했습니다. DB 저장 이전에 validation 체크를 진행할 수 있도록 각 model 선언 시에 field validator를 추가했습니다. 이메일 필드는 models.EmailField를 이용해서 내장 email validation을 적용했습니다.

중복해서 사용되는 validator의 코드 재사용성을 높이기 위해 core 앱 내부에 validators.py를 만들어 validator들을 모두 저장했습니다.

```python
## core.validators.py
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


## account.models.py
from core.validators import DateValidator, PhoneValidator

class Applyment(models.Model):
    birth_date = models.DateField(validators=[DateValidator])
    phone = models.CharField(validators=[PhoneValidator], max_length=15)
    ...


## gallery.models.py
from core.validators import ArtworkPriceValidator, ArtworkSizeValidator

class Artwork(models.Model):
    price = models.IntegerField(validators=[ArtworkPriceValidator])
    size = models.IntegerField(validators=[ArtworkSizeValidator])
    ...
```

#### 작가 등록신청 관리 validation

작가 등록신청을 하면 Applyment 객체가 생성됩니다. 승인 여부는 is_approved와 is_rejected 필드를 이용해서 처리됩니다.

> ### Authorization

#### 유저 권한 설정 mixin

AccessMixin을 상속받아 ArtistRequiredMixin과 ManagerOnlyMixin을 구현했습니다. Custom Mixin을 상속받아 각 view class 내부에서 권한확인 코드의 반복을 줄였습니다.

```python
## core.mixins.py
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
```

> ### Errors

#### 400_BAD_REQUEST

#### 401_NOT_AUTHORIZED

#### 404_NOT_FOUND
