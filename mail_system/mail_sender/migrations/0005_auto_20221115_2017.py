# Generated by Django 3.0.5 on 2022-11-15 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_sender', '0004_mailing_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailinguser',
            name='sending_time',
        ),
        migrations.AddField(
            model_name='mailing',
            name='sending_time',
            field=models.DateTimeField(null=True, verbose_name='Дата отправки'),
        ),
    ]
