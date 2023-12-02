from django.core.exceptions import ValidationError 


def ArtworkPriceValidator(value):
    if type(value) != int or value < 0:
        raise ValidationError("0 이상의 숫자를 입력하세요")
    

def ArtworkSizeValidator(value):
    if type(value) != int or not (1 <= value <= 500):

        raise ValidationError("1 이상 500 이하의 숫자를 입력하세요")