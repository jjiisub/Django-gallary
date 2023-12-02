from django.core.exceptions import ValidationError 

def ApproveRejectValidator(approve_list, reject_list):
    if set(approve_list) & set(reject_list):
        raise ValidationError("승인과 반려를 동시에 체크할 수 없습니다.")