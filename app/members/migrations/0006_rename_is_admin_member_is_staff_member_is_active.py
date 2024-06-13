# Generated by Django 5.0.6 on 2024-06-12 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_remove_member_member_password_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='is_admin',
            new_name='is_staff',
        ),
        migrations.AddField(
            model_name='member',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
