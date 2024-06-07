from django.db import models

# Create your models here.
class CardSet(models.Model):
    cardset_title=models.CharField(max_length=255)
    cardset_public = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at= models.DateTimeField()
    folder = models.ForeignKey('Folder',on_delete=False)
    member = models.ForeignKey('Member',on_delete=models.CASCADE)

    class Meta:
        db_table = 'Cardset'
