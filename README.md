# Introduction

### Environment

- Python 3.11.6
- Django 4.2.7

### Deployment

- [https://develearn.co.kr](https://develearn.co.kr)

### Test Account

| Username | Password | Authority |
| <img width=33%/> | <img width=33%/> | <img width=33%/> |
| admin | admin | Admin |
| manager | adminadmin11 | Manager |
| user1 | useruser11 | Artist |
| user4 | useruser44 | User(not Artist) |

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

# Structure

### Database Schema

Schema Diagram

### Server

![ServerDiagram](https://github.com/jjiisub/Django-gallery/assets/89283288/71d20fc3-e889-4a6a-90db-caac1a99663a)

### Endpoints

|       App        |            Path            |         Description          |
| :--------------: | :------------------------: | :--------------------------: |
| <img width=20%/> |      <img width=40%/>      |       <img width=40%/>       |
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

### 기능 구현

- #### [작품 등록 가격 콤마 표시](https://github.com/jjiisub/Django-gallery/wiki/작품등록-가격-콤마표시)

- #### [전시등록 시 작품목록출력](https://github.com/jjiisub/Django-gallery/wiki/전시등록-작품목록-form)

- #### [작가등록신청관리 일괄처리](https://github.com/jjiisub/Django-gallery/wiki/작가등록신청관리-일괄처리)

- #### [작가 통계](https://github.com/jjiisub/Django-gallery/wiki/작가-통계)

### Validation

- #### [Field Validation](https://github.com/jjiisub/Django-gallery/wiki/Field-Validation)

- #### [작가등록신청관리 validation](https://github.com/jjiisub/Django-gallery/wiki/작가-등록신청-관리-validation)

### Authorization

- #### [유저 권한 설정 mixin](https://github.com/jjiisub/Django-gallery/wiki/유저-권한-설정-mixin)

### 추가요구사항 구현

- #### [작가/작품 검색](https://github.com/jjiisub/Django-gallery/wiki/작가-작품-검색)

- #### [작가등록신청관리 검색](https://github.com/jjiisub/Django-gallery/wiki/작가등록신청관리-검색)

- #### [작가등록신청관리 CSV 다운로드](https://github.com/jjiisub/Django-gallery/wiki/작가등록신청관리-CSV-다운로드)

### Error Pages

- #### [401_NOT_AUTHORIZED](https://github.com/jjiisub/Django-gallery/wiki/401_NOT_AUTHORIZED)

- #### [404_NOT_FOUND](https://github.com/jjiisub/Django-gallery/wiki/404_NOT_FOUND)
