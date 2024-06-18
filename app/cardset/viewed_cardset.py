from django.utils.deprecation import MiddlewareMixin
from .models import CardSet
from django.shortcuts import get_object_or_404

class TrackViewedCardSetMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.member.is_authenticated and 'viewed_at' in view_kwargs:
            post = get_object_or_404(CardSet, id=view_kwargs['viewed_at'])
            CardSet.objects.create(user=request.member, post=post)
        return None
