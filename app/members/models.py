from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class MemberManager(models.Manager):
    def create_user(self, account, member_email, display_name, password=None):
        if not member_email:
            raise ValueError("Users must have an email address")
        user = self.model(
            account=account,
            member_email=member_email,
            display_name=display_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, account, member_email, display_name, password):
        user = self.create_user(
            account=account,
            member_email=member_email,
            display_name=display_name,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user
    
    def get_by_natural_key(self, account):
        return self.get(account=account)

class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=50)
    member_email = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    daily_accom = models.FloatField(default=0.0)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MemberManager()

    USERNAME_FIELD = "account"
    REQUIRED_FIELDS = ["member_email", "display_name"]

    def __str__(self):
        return self.account

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    class Meta:
        db_table = "Member"
        managed = True
