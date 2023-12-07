<details>
<summary><Strong>Table of Contents</strong></summary>
<div markdown="1">
<br>

> ### [Introduction](#introduction-1)
>
> - Environment
> - Deployment
> - Test Accounts
>
> ### [Structure](#structure-1)
>
> - DB Schema
> - Server Structure
> - Endpoints
>
> ### [Features](#features-1)
>
> - 기본요구사항
> - 추가요구사항
>
> ### [Demo](#demo-1)
>
> ### [Installation](#installation-1)
>
> ### [Room For Improvement](#room-for-improvement-1)

</div>
</details>

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
|        <img width=200/>        |   <img width=300/>    |                    <img width=50/>                     | <img width=100/> |                                              <img width=300/>                                               |
|  <strong>고객 페이지</strong>  |       회원가입        |    [link](https://develearn.co.kr/account/signup/)     |        -         |                                                      -                                                      |
|                                |        로그인         |     [link](https://develearn.co.kr/account/login/)     |        -         |           [로그인 성공 페이지](https://github.com/jjiisub/Django-gallery/wiki/로그인-성공-페이지)           |
|                                |     작가목록 조회     |      [link](https://develearn.co.kr/artist/list/)      |        -         |                                                      -                                                      |
|                                |     작품목록 조회     |     [link](https://develearn.co.kr/artwork/list/)      |        -         |                                                      -                                                      |
|                                |     작가등록 신청     |     [link](https://develearn.co.kr/account/apply/)     |      `User`      |                                                      -                                                      |
| <strong>관리자 페이지</strong> |       대시보드        |   [link](https://develearn.co.kr/account/dashboard/)   |    `Manager`     |                                                      -                                                      |
|                                | 작가등록신청내역 조회 |   [link](https://develearn.co.kr/management/apply/)    |    `Manager`     |            [일괄처리](https://github.com/jjiisub/Django-gallery/wiki/작가등록신청관리-일괄처리)             |
|                                |       작가통계        | [link](https://develearn.co.kr/management/statistics/) |    `Manager`     |                    [통계 계산](https://github.com/jjiisub/Django-gallery/wiki/작가-통계)                    |
|  <strong>작가 페이지</strong>  |       대시보드        |   [link](https://develearn.co.kr/account/dashboard/)   |     `Artist`     |                                                      -                                                      |
|                                |       작품등록        |    [link](https://develearn.co.kr/artwork/create/)     |     `Artist`     |            [가격콤마표시](https://github.com/jjiisub/Django-gallery/wiki/작품등록-가격-콤마표시)            |
|                                |       전시등록        |   [link](https://develearn.co.kr/exhibition/create/)   |     `Artist`     |            [작품목록출력](https://github.com/jjiisub/Django-gallery/wiki/전시등록-작품목록-form)            |
|     <strong>공통</strong>      |      Validation       |                           -                            |        -         |             [Field Validation](https://github.com/jjiisub/Django-gallery/wiki/Field-Validation)             |
|                                |                       |                           -                            |        -         | [작가등록신청관리 validation](https://github.com/jjiisub/Django-gallery/wiki/작가-등록신청-관리-validation) |
|                                |     Authorization     |                           -                            |        -         |             [권한 Mixins](https://github.com/jjiisub/Django-gallery/wiki/유저-권한-설정-mixin)              |
|                                |      Error Pages      |                           -                            |        -         |             [Validation Error](https://github.com/jjiisub/Django-gallery/wiki/Validation-Error)             |
|                                |                       |                           -                            |        -         |           [401_NOT_AUTHORIZED](https://github.com/jjiisub/Django-gallery/wiki/401_NOT_AUTHORIZED)           |
|                                |                       |                           -                            |        -         |                [404_NOT_FOUND](https://github.com/jjiisub/Django-gallery/wiki/404_NOT_FOUND)                |

### 추가요구사항

- [검색 기능](https://github.com/jjiisub/Django-gallery/wiki/검색-기능)

- [작가등록신청관리 CSV 다운로드](https://github.com/jjiisub/Django-gallery/wiki/작가등록신청관리-CSV-다운로드)

- [추가 작가별 통계치](https://github.com/jjiisub/Django-gallery/wiki/추가-작가별-통계치)

- [쿼리 최적화](https://github.com/jjiisub/Django-gallery/wiki/DB-쿼리-최적화)

# Demo

### 고객 페이지

|                                                            메인페이지                                                             |                                                               로그인                                                                |                                                               회원가입                                                                |
| :-------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------: |
| <img width="300" alt="메인" src="https://github.com/jjiisub/Django-gallery/assets/89283288/04464c66-2278-47ac-a914-a7e33456da93"> | <img width="300" alt="로그인" src="https://github.com/jjiisub/Django-gallery/assets/89283288/d57a582b-05d9-47b1-9950-ee90c664d132"> | <img width="300" alt="회원가입" src="https://github.com/jjiisub/Django-gallery/assets/89283288/72bf5f82-56c1-4e15-9ec8-aec7927412f7"> |

|                                                               작가목록 조회                                                                |                                                               작품목록 조회                                                                |                                                               작가등록 신청                                                                |
| :----------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------: |
| <img width="300" alt="고객-작가목록" src="https://github.com/jjiisub/Django-gallery/assets/89283288/f2d742a9-58c3-4f73-95ac-6b8a3862ac4a"> | <img width="300" alt="고객-작품목록" src="https://github.com/jjiisub/Django-gallery/assets/89283288/1a106ecf-891f-4d1b-9b01-f2ff47025b9f"> | <img width="300" alt="고객-작가신청" src="https://github.com/jjiisub/Django-gallery/assets/89283288/d4c88aeb-f13b-4f55-85c2-23d5d8f91a9f"> |

### 관리자 페이지

|                                                                   대시보드                                                                   |                                                             작가등록신청내역조회                                                             |                                                                 작가통계                                                                 |
| :------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------: |
| <img width="300" alt="관리자-대시보드" src="https://github.com/jjiisub/Django-gallery/assets/89283288/7cae8688-2ea2-4ad1-b95b-55f532e6de83"> | <img width="300" alt="관리자-등록관리" src="https://github.com/jjiisub/Django-gallery/assets/89283288/0ba4b52d-3bca-4800-ab82-9280103c6f3b"> | <img width="300" alt="관리자-통계" src="https://github.com/jjiisub/Django-gallery/assets/89283288/d0fcae67-0f1a-4f4d-9a98-c3fc84427215"> |

### 작가 페이지

|                                                                  대시보드                                                                  |                                                                  작품등록                                                                  |                                                                  전시등록                                                                  |
| :----------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------: |
| <img width="300" alt="작가-대시보드" src="https://github.com/jjiisub/Django-gallery/assets/89283288/d46bf921-5af5-4bcc-952c-2e2e41f85664"> | <img width="300" alt="작가-작품등록" src="https://github.com/jjiisub/Django-gallery/assets/89283288/36f0246e-9665-4833-a8ee-0c64af60ab71"> | <img width="300" alt="작가-전시등록" src="https://github.com/jjiisub/Django-gallery/assets/89283288/acb2b20d-7c51-4efd-a1d8-fceec943b97b"> |

### 에러 페이지

|                                                    401_UNAUTHORIZED                                                    |                                                     404_NOT_FOUND                                                      |
| :--------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------: |
| <img width="500" src="https://github.com/jjiisub/Django-gallery/assets/89283288/b02f9432-ecb6-4aaa-9c88-f92f9573ceb8"> | <img width="500" src="https://github.com/jjiisub/Django-gallery/assets/89283288/0b116fa4-5fee-454d-88ec-3d284b79bb69"> |

# Installation

### Download

```bash
$ git clone https://github.com/jjiisub/Django-gallery.git
```

### Prerequisites

```bash
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

- [작품등록 가격콤마 출력](https://github.com/jjiisub/Django-gallery/wiki/작품등록-가격콤마-Number-함수)

- [작가등록신청관리 일괄처리](https://github.com/jjiisub/Django-gallery/wiki/작가등록신청관리-일괄처리-Transaction)

- [DB "created_at" Field Index](https://github.com/jjiisub/Django-gallery/wiki/DB-Index)
