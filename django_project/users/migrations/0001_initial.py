# Generated by Django 2.0.4 on 2018-06-22 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=20)),
                ('email_address', models.CharField(max_length=40, unique=True)),
                ('register_date', models.DateTimeField()),
            ],
        ),
    ]
