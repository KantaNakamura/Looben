# Generated by Django 4.0.6 on 2022-09-10 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_change_connection_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='schools',
            name='number_of_viewer',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='users',
            name='picture',
            field=models.FileField(blank=True, default='pfp/unknown_user.png', upload_to='pfp/'),
        ),
    ]
