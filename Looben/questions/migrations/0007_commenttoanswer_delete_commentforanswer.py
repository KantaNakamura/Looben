# Generated by Django 4.0.6 on 2022-10-12 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0006_alter_commentforanswer_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentToAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=250)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.answerforquestion')),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '回答に対する質問',
                'db_table': 'comment_to_answer',
            },
        ),
        migrations.DeleteModel(
            name='CommentForAnswer',
        ),
    ]
