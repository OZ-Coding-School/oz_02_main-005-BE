from django.contrib.auth.backends import BaseBackend
from .models import Member

class MemberBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Member.objects.get(account=username)
        except Member.DoesNotExist:
            return None

        if user.check_password(password) and user.is_active:
            return user

    def get_user(self, member_id):
        try:
            return Member.objects.get(member_id=member_id)
        except Member.DoesNotExist:
            return None
