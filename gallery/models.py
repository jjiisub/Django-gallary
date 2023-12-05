from django.db import models

from account.models import User

from core.validators import DateValidator, ArtworkPriceValidator, ArtworkSizeValidator


class Artist(models.Model):
    '''
    작가 모델

    Fields:
        user(FK):           유저
        name(Char):         작가 이름
        gender(Char):       작가 성별
        birth_date(Date):   작가 생년월일
        email(Email):       작가 이메일
        phone(Char):        작가 연락처
        created_at(Date):   작가 등록일
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=5)
    birth_date = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Artist 모델 출력 method'''
        return self.name


class Artwork(models.Model):
    '''
    작품 모델

    Fields:
        artist(FK):         작가
        title(Char):        작품 제목
        price(Int):         작품 가격
        size(Int):          작품 호수
        created_at(Date):   작품 등록일
    '''
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='artworks')
    title = models.CharField(max_length=64)
    price = models.IntegerField(validators=[ArtworkPriceValidator])
    size = models.IntegerField(validators=[ArtworkSizeValidator])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Artwork 모델 출력 method'''
        return self.title


class Exhibition(models.Model):
    '''
    전시 모델

    Fields:
        artist(FK):         작가
        title(Char):        전시 제목
        start_date(Date):   전시 시작일
        end_date(Date):     전시 종료일
        artworks(List):     전시 작품목록
    '''
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='exhibitions')
    title = models.CharField(max_length=64)
    start_date = models.DateField(validators=[DateValidator])
    end_date = models.DateField(validators=[DateValidator])
    artworks = models.ManyToManyField(Artwork, related_name='exhibitions')

    def __str__(self):
        '''Exhibition 모델 출력 method'''
        return self.title
