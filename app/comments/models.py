from django.db import models
#from members.models import Member
#from cardsets.models import Cardset

# Create your models here.
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    #member = models.ForeignKey(Member, on_delete=models.CASCADE)
    #cardset = models.ForeignKey(Cardset, on_delete=models.CASCADE)
    parent = models.ForeignKey('self',related_name='reply', on_delete=models.CASCADE, null=True, blank=True)