# Generated by Django 2.0.4 on 2018-06-24 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0007_userexamrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='userwordsplan',
            name='examine_words',
            field=models.IntegerField(default=20),
        ),
    ]
