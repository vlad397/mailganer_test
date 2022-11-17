from django.contrib import admin
from django.urls import path

from mail_sender import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('read_mail/<int:pk>/', views.track_clicking, name='track'),
    path('unsubscribe/<str:mail>/', views.unsubscribe, name='unsubscribe'),
]
