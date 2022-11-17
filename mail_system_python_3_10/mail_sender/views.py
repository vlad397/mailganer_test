from django.http import HttpResponse

from .models import MailingUser, User


def track_clicking(request, pk: int) -> HttpResponse:
    if request.method == 'GET':
        mailing_user = MailingUser.objects.get(pk=pk)
        if mailing_user:
            mailing_user.is_seen = True
            mailing_user.save()
    return HttpResponse('Спасибо за просмотр!')


def unsubscribe(request, mail: str) -> HttpResponse:
    if request.method == 'GET':
        user = User.objects.get(email=mail)
        if user:
            user.is_subscribed = False
            user.save()
    return HttpResponse('Вы отписались от рассылки')
