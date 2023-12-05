# Introduction

### Environment

- Python 3.11.6
- Django 4.2.7

### Deployment

- [https://develearn.co.kr](https://develearn.co.kr)

### Test Accounts

|     Authority      |     Username     |     Password     |
| :----------------: | :--------------: | :--------------: |
|  <img width=300/>  | <img width=300/> | <img width=300/> |
|      `Admin`       |      admin       |      admin       |
|     `Manager`      |     manager      |  adminadmin123   |
|      `Artist`      |      user1       |    useruser11    |
| `User(not Artist)` |      user4       |    useruser44    |

# Structure

### DB Schema

![DBSchema](https://github.com/jjiisub/Django-gallery/assets/89283288/4a77bcd9-353d-4ad9-870b-fc057db64b3e)

### Server Structure

![ServerDiagram](https://github.com/jjiisub/Django-gallery/assets/89283288/e80aad4c-8831-468e-a00d-1c2a5ac1f276)

### Endpoints

|       App        |            Path            |         Description          |
| :--------------: | :------------------------: | :--------------------------: |
| <img width=100/> |      <img width=400/>      |       <img width=400/>       |
|    `account`     |      account/signup/       |           회원가입           |
|                  |       account/login/       |            로그인            |
|                  |      account/logout/       |           로그아웃           |
|                  |       account/apply/       |         작가등록신청         |
|                  |     account/dashboard/     |    대시보드(작가/관리자)     |
|    `gallery`     |             /              |          메인페이지          |
|                  |        artist/list/        |        작가 목록조회         |
|                  |       artist/search/       |          작가 검색           |
|                  |       artwork/list/        |        작품 목록조회         |
|                  |      artwork/search/       |          작품 검색           |
|                  |      artwork/create/       |          작품 등록           |
|                  |     exhibition/create/     |          전시 등록           |
|   `management`   |     management/apply/      |       작가등록신청관리       |
|                  |  management/apply/search/  |    작가등록신청관리 검색     |
|                  | management/apply/download/ | 작가등록신청관리 CSV다운로드 |
|                  |   management/statistics/   |          작가 통게           |

# Features

### 기본요구사항

|              Role              |        Detail         |                          Link                          |    Authority     |                                                   Issues                                                    |
| :----------------------------: | :-------------------: | :----------------------------------------------------: | :--------------: | :---------------------------------------------------------------------------------------------------------: |
|        <img width=200/>        |   <img width=200/>    |                    <img width=50/>                     | <img width=200/> |                                              <img width=300/>                                               |
|  <strong>고객 페이지</strong>  |       회원가입        |    [link](https://develearn.co.kr/account/signup/)     |        -         |                                                      -                                                      |
|                                |        로그인         |     [link](https://develearn.co.kr/account/login/)     |        -         |                                             로그인 성공 페이지                                              |
|                                |     작가목록 조회     |      [link](https://develearn.co.kr/artist/list/)      |        -         |                                                      -                                                      |
|                                |     작품목록 조회     |     [link](https://develearn.co.kr/artwork/list/)      |        -         |                                                      -                                                      |
|                                |     작가등록 신청     |     [link](https://develearn.co.kr/account/apply/)     |      `User`      |                                                                                                             |
| <strong>관리자 페이지</strong> |       대시보드        |   [link](https://develearn.co.kr/account/dashboard/)   |    `Manager`     |                                                                                                             |
|                                | 작가등록신청내역 조회 |   [link](https://develearn.co.kr/management/apply/)    |    `Manager`     |            [일괄처리](https://github.com/jjiisub/Django-gallery/wiki/작가등록신청관리-일괄처리)             |
|                                |       작가통계        | [link](https://develearn.co.kr/management/statistics/) |    `Manager`     |                    [통계 계산](https://github.com/jjiisub/Django-gallery/wiki/작가-통계)                    |
|  <strong>작가 페이지</strong>  |       대시보드        |   [link](https://develearn.co.kr/account/dashboard/)   |     `Artist`     |                                                                                                             |
|                                |       작품등록        |    [link](https://develearn.co.kr/artwork/create/)     |     `Artist`     |            [가격콤마표시](https://github.com/jjiisub/Django-gallery/wiki/작품등록-가격-콤마표시)            |
|                                |       전시등록        |   [link](https://develearn.co.kr/exhibition/create/)   |     `Artist`     |            [작품목록출력](https://github.com/jjiisub/Django-gallery/wiki/전시등록-작품목록-form)            |
|     <strong>공통</strong>      |      Validation       |                           -                            |        -         |             [Field Validation](https://github.com/jjiisub/Django-gallery/wiki/Field-Validation)             |
|                                |                       |                           -                            |        -         | [작가등록신청관리 validation](https://github.com/jjiisub/Django-gallery/wiki/작가-등록신청-관리-validation) |
|                                |     Authorization     |                           -                            |        -         |             [권한 Mixins](https://github.com/jjiisub/Django-gallery/wiki/유저-권한-설정-mixin)              |
|                                |      Error Pages      |                           -                            |        -         |            [Form Validation Error](https://github.com/jjiisub/Django-gallery/wiki/404_NOT_FOUND)            |
|                                |                       |                           -                            |        -         |           [401_NOT_AUTHORIZED](https://github.com/jjiisub/Django-gallery/wiki/401_NOT_AUTHORIZED)           |
|                                |                       |                           -                            |        -         |                [404_NOT_FOUND](https://github.com/jjiisub/Django-gallery/wiki/404_NOT_FOUND)                |

### 추가요구사항

- [작가 검색](https://github.com/jjiisub/Django-gallery/wiki/작가-작품-검색)

- [작품 검색]()

- [작가등록신청관리 검색](https://github.com/jjiisub/Django-gallery/wiki/작가등록신청관리-검색)

- [작가등록신청관리 CSV 다운로드](https://github.com/jjiisub/Django-gallery/wiki/작가등록신청관리-CSV-다운로드)

# Screenshots

    ![사진입니다]()

# Installation

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
DEBUG=False
SERVER_IP='YourServerIP'
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

# Room For Improvement

- 가격콤마표시 Number 함수 크기 제한
