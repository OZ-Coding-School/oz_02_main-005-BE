from django.contrib.auth import get_user_model

def filter_users_by_email(email, prefer_verified=False):
    """ Return all users by email address """
    User = get_user_model()
    if prefer_verified:
        # Using the query that `allauth` would typically use but adjusted for `member_email`
        return User.objects.filter(member_email__iexact=email, emailaddress__verified=True)
    return User.objects.filter(member_email__iexact=email)
