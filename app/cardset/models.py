from django.db import models

# Create your models here.
class CardSet(models.Model):
    cardset_title=models.CharField(max_length=255)
    cardset_public = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at= models.DateTimeField()
    cardset_down = models.BooleanField(default=True)
    cardset_count = models.IntegerField(default=0)
    #folder = models.ForeignKey('Folder',on_delete=models.CASCADE)
    #member = models.ForeignKey('Member',on_delete=models.CASCADE)

    class Meta:
        db_table = 'Cardset'
