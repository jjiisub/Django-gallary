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

### .env File

```shell
## .env

SECRET_KEY="YourSecretKey"
DEBUG=True
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

### 기능 구현

- #### 작품 등록 가격 콤마 표시

작품 등록 페이지에서 가격을 입력할 때, 천 단위마다 콤마를 출력하는 기능을 JavaScript로 구현했습니다. 가격 element에 입력이 될 때마다 입력값이 숫자 형식인지 확인하고, 천 단위마다 콤마를 삽입합니다. 제출 버튼을 누르면 콤마를 제거한 값을 form으로 넘겨줍니다.

```js
// gallery/templates/gallery/artwork_create.html
const el = document.getElementById("price");
const btn = document.getElementById("btn-submit");
function ChangeToNumber(value) {
  return Number(value.replace(/\,/g, ""));
}

el.addEventListener("input", function () {
  const price = el.value;
  const price_num = ChangeToNumber(price);
  if (isNaN(price_num) == true || price_num == 0) {
    el.value = "";
  } else {
    el.value = price_num.toLocaleString();
  }
});

btn.addEventListener("click", function () {
  el.value = ChangeToNumber(el.value);
});
```

- #### 작가, 작품 검색 기능

작가 목록 페이지에서는 이름, 성별, 생년월일, 이메일, 연락처를 기준으로 키워드를 입력하여 검색할 수 있습니다.

이름과 이메일은 django orm의 icontains를 이용하여 검색 키워드를 포함하는 결과를 출력합니다. 성별, 생년월일, 연락처는 키워드와 일치하는 결과를 출력합니다. 이때 검색 기준에 따라 placeholder를 변경하여 검색 형식을 알 수 있도록 구현했습니다.

```python
## gallery/views.py
class ArtistSearchView(ListView):
    ...
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
```

```js
// gallery/templates/gallery/artwork_list.html
const searchOptionEl = document.getElementById("search-option");
const searchKeywordEl = document.getElementById("search-keyword");
searchOptionEl.addEventListener("change", function () {
  const searchOptionValue = searchOptionEl.options[searchOptionEl.selectedIndex].value;
  if (searchOptionValue == "gender") {
    searchKeywordEl.setAttribute("placeholder", "m(남자) 또는 f(여자)");
  } else if (searchOptionValue == "birth_date") {
    searchKeywordEl.setAttribute("placeholder", "YYYY-MM-DD");
  } else if (searchOptionValue == "phone") {
    searchKeywordEl.setAttribute("placeholder", "000-0000-0000");
  } else {
    searchKeywordEl.setAttribute("placeholder", "검색 키워드를 입력하세요");
  }
});
```

작품 목록 페이지에서는 제목, 가격, 호수를 기준으로 키워드를 입력하여 검색할 수 있습니다.

검색 화면에서 가격 또는 호수를 선택하면 비교기준(이상, 이하)를 정해 입력값과 비교하여 검색할 수 있습니다. 선택한 검색기준, 비교기준, 키워드를 GET query string으로 전달받습니다. 유저가 임의의 값을 전달하는 경우를 대비하여 try/except로 예외처리하였습니다.

검색 화면에서 제목을 선택하면 비교기준 선택이 비활성화됩니다. 제목은 django orm의 icontains를 이용하여 키워드를 포함하는 결과를 출력합니다.

```python
## gallery.views.py
class ArtworkSearchView(ListView):
    ...
    def get_queryset(self):
        option = self.request.GET.get("search-option")
        keyword = self.request.GET.get("search-keyword")
        queryset = []
        if option=='title':
            queryset = Artwork.objects.filter(title__icontains=keyword)
        elif option=='price' or option=='size':
            comp = self.request.GET.get("search-option-compare")
            option_compare = '__gte' if comp=="more" else '__lte'
            try:
                queryset = Artwork.objects.filter(**{f'{option}{option_compare}': keyword})
            except:
                pass
        return queryset
```

```js
const searchOptionEl = document.getElementById("search-option");
const searchOptionCompareEl = document.getElementById("search-option-compare");
searchOptionEl.addEventListener("change", function () {
  const searchOptionValue = searchOptionEl.options[searchOptionEl.selectedIndex].value;
  if (searchOptionValue == "title") {
    searchOptionCompareEl.setAttribute("disabled", true);
  } else {
    searchOptionCompareEl.removeAttribute("disabled");
  }
});
```

- #### 작가등록신청 검색

작가 검색과 동일한 방법으로 구현했습니다. ManagerOnlyMixin을 상속받아 권한 확인을 구현했습니다.

```python
## management/views.py
class ApplymentSearchView(ManagerOnlyMixin, ListView):
    ...
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
```

- #### 작가등록신청 일괄처리

approve_list, reject_list에는 각각 승인, 반려가 선택된 applyment 객체 목록이 담겨있습니다. 각 리스트를 서버 상에서 순회하면서 업데이트하면 쿼리가 여러번 수행되기 때문에 비효율적이라고 판단했습니다. 따라서 한 번의 쿼리로 리스트에 담긴 객체들을 모두 업데이트하도록 구현했습니다.

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

- #### 작가등록신청 CSV 다운로드

... 그냥 feature이긴 한데

```python
## management/views.py
class ApplymentDownloadView(ManagerOnlyMixin, View):
    def get(self, request):
        applyments = Applyment.objects.all().order_by('-created_at')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="applyments.csv"'
        writer = csv.writer(response)
        writer.writerow(['이름', '성별', '생년월일','이메일','연락처','신청 일시','승인', '반려'])
        for applyment in applyments:
            gender_value = '남성' if applyment.gender=='m' else '여성'
            is_approved_value = 'v' if applyment.is_approved else ''
            is_rejected_value = 'v' if applyment.is_rejected else ''
            writer.writerow([applyment.name, gender_value, applyment.birth_date, applyment.email, applyment.phone, applyment.created_at, is_approved_value, is_rejected_value])
        return response
```

- #### 작가 통계

### Validation

- #### Form Field Validation

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

- #### 작가 등록신청 관리 validation

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

- #### 전시 등록 페이지 작품 목록 form

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

### Authorization

- #### 유저 권한 설정 mixin

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

### Error Pages

- #### 400_BAD_REQUEST

- #### 401_NOT_AUTHORIZED

- #### 404_NOT_FOUND
