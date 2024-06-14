from django.db import models
#from members.models import Member

# Create your models here.
class Folder(models.Model):
    folder_title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    #member = models.ForeignKey(Member, on_delete=models.CASCADE)