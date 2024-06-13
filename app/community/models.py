from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


# Create your models here.

class MemberManager(BaseUserManager):
    def create_user(self, email, display_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, display_name=display_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, display_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, display_name, password, **extra_fields)

class Member(AbstractBaseUser):
    member_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Increased length for hashed passwords
    signup_purpose = models.CharField(max_length=255)
    security_answer = models.CharField(max_length=255)
    security_question = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    daily_accom = models.FloatField(default=0.0)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['display_name']

    def __str__(self):
        return self.email


class Folder(models.Model):
    folder_id = models.AutoField(primary_key=True)
    folder_title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return self.folder_title

class Cardset(models.Model):
    cardset_id = models.AutoField(primary_key=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    cardset_title = models.CharField(max_length=255)
    cardset_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    cardset_down = models.BooleanField(default=True)
    down_count = models.IntegerField(default=0)

    def __str__(self):
        return self.cardset_title

class Card(models.Model):
    card_id = models.AutoField(primary_key=True)
    cardset = models.ForeignKey(Cardset, on_delete=models.CASCADE)
    card_question = models.TextField()
    card_answer = models.TextField()
    question_type = models.BooleanField(default=True)
    question_option = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.card_question

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
