# Generated by Django 2.0.4 on 2018-06-23 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0002_userdefinedwords_userrecitedbookwords_userreciteddefinedwords'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbook',
            name='book',
        ),
        migrations.RemoveField(
            model_name='userbook',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userdefinedwords',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userrecitedbookwords',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userrecitedbookwords',
            name='word',
        ),
        migrations.RemoveField(
            model_name='userreciteddefinedwords',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userreciteddefinedwords',
            name='word',
        ),
        migrations.DeleteModel(
            name='UserBook',
        ),
        migrations.DeleteModel(
            name='UserDefinedWords',
        ),
        migrations.DeleteModel(
            name='UserRecitedBookWords',
        ),
        migrations.DeleteModel(
            name='UserRecitedDefinedWords',
        ),
    ]
