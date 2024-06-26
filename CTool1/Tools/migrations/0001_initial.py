# Generated by Django 4.2.11 on 2024-05-18 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal', models.IntegerField(choices=[(1, 'Web App'), (2, 'Network'), (3, 'Cloud')])),
                ('typeS', models.IntegerField(choices=[(1, 'Web-Based'), (2, 'Mobile'), (3, 'Network')])),
                ('toolsC', models.IntegerField(choices=[(1, 'Web App'), (2, 'Network'), (3, 'Code Analysis'), (4, 'Password Cracking')])),
                ('platform', models.IntegerField(choices=[(1, 'Windows'), (2, 'Linux'), (3, 'MacOS'), (4, 'Cloud')])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
