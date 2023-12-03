import re
# import datetime

from django.core.exceptions import ValidationError


def DateValidator(value):
    pattern = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$')
    if not bool(pattern.match(str(value))):
        raise ValidationError("YYYY-MM-DD 형식의 날짜를 입력하세요.")


def PhoneValidator(value):
    pattern = re.compile(r'^\d{3}-\d{4}-\d{4}$')
    if not bool(pattern.match(value)):
        raise ValidationError("000-0000-0000 형식의 연락처를 입력하세요.")


def ArtworkPriceValidator(value):
    if type(value) != int or value < 0:
        raise ValidationError("0 이상의 숫자를 입력하세요")


def ArtworkSizeValidator(value):
    if type(value) != int or not (1 <= value <= 500):
        raise ValidationError("1 이상 500 이하의 숫자를 입력하세요")


def ApproveRejectValidator(approve_list, reject_list):
    if set(approve_list) & set(reject_list):
        raise ValidationError("승인과 반려를 동시에 체크할 수 없습니다.")