# Generated by Django 4.0.6 on 2022-08-24 11:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='connection',
            field=models.ManyToManyField(blank=True, related_name='connected_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='users',
            name='picture',
            field=models.FileField(blank=True, default='pfp/Looben.jpg', upload_to='pfp/'),
        ),
    ]
