from django.db import migrations, models
from django.db.models.functions import Lower

def forwards(apps, schema_editor):
    Member = apps.get_model('members', 'Member')
    email_field = 'member_email'
    Member.objects.all().exclude(**{email_field: Lower(email_field)}).update(
        **{email_field: Lower(email_field)}
    )

class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_remove_member_last_login_member_is_superuser_and_more'),
        ('account', '0005_emailaddress_idx_upper_email'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
