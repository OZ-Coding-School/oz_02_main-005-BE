from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('verified', models.BooleanField(default=False)),
                ('primary', models.BooleanField(default=False)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Member')),
            ],
            options={
                'db_table': 'emailaddress',
            },
        ),
    ]
