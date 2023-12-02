import re

from django.core.exceptions import ValidationError


def PhoneValidator(value):

    pattern = re.compile(r'^\d{3}-\d{4}-\d{4}$')

    if not bool(pattern.match(value)):
        raise ValidationError("000-0000-0000 형식의 연락처를 입력하세요.")