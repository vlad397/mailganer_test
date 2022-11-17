from django.conf.urls import url
from django.contrib import admin

from mail_sender import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^read_mail/(?P<pk>[0-9]+)/$', views.track_clicking),
    url(r'^unsubscribe/(?P<mail>.+)/$', views.unsubscribe),
]
