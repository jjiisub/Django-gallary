import re

from django.core.exceptions import ValidationError


def DateValidator(value):
    '''
    날짜 field validation 함수

    Args:
        value:  form에 입력된 날짜 값

    Raises:
        ValidationError:    입력값이 YYYY-MM-DD 형식이 아닌 경우
    '''
    pattern = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$')
    if not bool(pattern.match(str(value))):
        raise ValidationError("YYYY-MM-DD 형식의 날짜를 입력하세요.")


def PhoneValidator(value):
    '''
    연락처 field validation 함수

    Args:
        value:  form에 입력된 전화번호 값

    Raises:
        ValidationError:    입력값이 000-0000-0000 형식이 아닌 경우
    '''
    pattern = re.compile(r'^\d{3}-\d{4}-\d{4}$')
    if not bool(pattern.match(value)):
        raise ValidationError("000-0000-0000 형식의 연락처를 입력하세요.")


def ArtworkPriceValidator(value):
    '''
    작품 가격 field validation 함수

    Args:
        value:  form에 입력된 작품 가격 값

    Raises:
        ValidationError:    입력값이 0 이상의 숫자가 아닌 경우
    '''
    if type(value) != int or value < 0:
        raise ValidationError("0 이상의 숫자를 입력하세요")


def ArtworkSizeValidator(value):
    '''
    작품 호수 field validation 함수

    Args:
        value:  form에 입력된 작품 호수 값

    Raises:
        ValidationError:    입력값이 1 이상 500 이하의 숫자가 아닌 경우
    '''
    if type(value) != int or not (1 <= value <= 500):
        raise ValidationError("1 이상 500 이하의 숫자를 입력하세요")


def ApproveRejectValidator(approve_list, reject_list):
    '''
    작가등록신청관리 validation 함수

    Args:
        approve_list(list): 승인이 선택된 Applyment PK 리스트
        reject_list(list):  반려가 선택된 Applyment PK 리스트

    Raises:
        ValidationError:    승인과 반려가 동시에 선택된 Applyment가 있는 경우
    '''
    if set(approve_list) & set(reject_list):
        raise ValidationError("승인과 반려를 동시에 체크할 수 없습니다.")
