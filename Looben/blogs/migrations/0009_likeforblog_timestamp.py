# Generated by Django 4.0.6 on 2022-11-18 02:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0008_blog_total_number_of_view_delete_totalnumberofview'),
    ]

    operations = [
        migrations.AddField(
            model_name='likeforblog',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
