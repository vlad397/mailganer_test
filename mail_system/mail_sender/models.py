from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import send_mails


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        error_messages={'unique': ('A user with that email already exists.')},
        verbose_name='Почта'
    )

    username = models.TextField(
        max_length=150, unique=True, verbose_name='Никнейм'
    )
    first_name = models.TextField(
        max_length=150, unique=True, verbose_name='Имя'
    )
    last_name = models.TextField(
        max_length=150, unique=True, verbose_name='Фамилия'
    )
    is_subscribed = models.BooleanField(
        default=True, verbose_name='Подписка на рассылку'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.username})'


class Mailing(models.Model):
    name = models.CharField(
        max_length=150, verbose_name='Название рассылки', unique=True,
        error_messages={'unique': ('Mailing with that name already exists.')}
    )
    subject = models.CharField(
        max_length=150, verbose_name='Тема рассылки'
    )
    body = models.TextField(
        verbose_name='Текст рассылки'
    )
    users = models.ManyToManyField(
        User, through='MailingUser', related_name='mail', verbose_name='Получатели'
    )
    sending_time = models.DateTimeField(
        verbose_name='Дата отправки', default=None, blank=True, null=True
    )

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return self.name


class MailingUser(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mailing', verbose_name='Получатель'
    )
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, related_name='mailing', verbose_name='Рассылка'
    )
    is_seen = models.BooleanField(
        default=False, verbose_name='Просмотрено'
    )

    class Meta:
        verbose_name = 'Рассылка - Пользователи'
        verbose_name_plural = 'Рассылки - Пользователи'

    def __str__(self):
        return f'{self.mailing} - {self.user}'


@receiver(post_save, sender=Mailing)
def create_profile(sender: Mailing, instance: Mailing, created: bool, **kwargs) -> bool:
    if created:
        subject = instance.subject
        body = instance.body
        sending_time = instance.sending_time

        users = User.objects.filter(is_subscribed=True)
        mail_info = {}

        for user in users:
            mailing_user = MailingUser.objects.create(user=user, mailing=instance)
            mail_info[user.email] = {'full_name': user.full_name(), 'mailing_user_id': mailing_user.id}

        if sending_time is None:
            send_mails.delay(mail_info, subject, body)
        else:
            send_mails.apply_async((mail_info, subject, body), eta=sending_time)
        
        return True
    return False
