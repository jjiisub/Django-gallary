from django.core.exceptions import ValidationError 

import re


def phone_validator(value):

    pattern = re.compile(r'^\d{3}-\d{4}-\d{4}$')

    if not bool(pattern.match(value)):
        raise ValidationError("000-0000-0000 형식으로 전화번호를 입력하세요.")