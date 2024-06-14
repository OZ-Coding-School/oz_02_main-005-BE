from django.db import models
from cardset.models import CardSet
# Create your models here.
class Card(models.Model):
    card_question = models.TextField()
    card_answer = models.TextField()
    question_type = models.BooleanField()
    question_option = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField()
    cardset=models.ForeignKey(CardSet,on_delete=models.CASCADE)
    class Meta:
        db_table = 'Card'