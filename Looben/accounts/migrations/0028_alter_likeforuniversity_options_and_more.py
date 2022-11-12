# Generated by Django 4.0.6 on 2022-11-11 05:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_rename_saveforuniversity_likeforuniversity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='likeforuniversity',
            options={'verbose_name': '大学いいね'},
        ),
        migrations.RemoveField(
            model_name='users',
            name='connection',
        ),
        migrations.RemoveField(
            model_name='users',
            name='saved_users',
        ),
        migrations.CreateModel(
            name='FollowForUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('followed_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'フォロー',
            },
        ),
    ]
