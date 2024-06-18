from django.db import models
from card.models import Member, Cardset
# Create your models here.

class Mileage(models.Model):
    mileage_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    mileage_amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.member.email} - {self.mileage_amount}'


class Rate(models.Model):
    rate_id = models.AutoField(primary_key=True)
    rate = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    cardset = models.ForeignKey(Cardset, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cardset.cardset_title} - {self.rate}'
