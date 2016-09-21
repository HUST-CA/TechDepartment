from django.conf.urls import url

from . import views

urlpatterns = [
    url('^welcome/$', views.WelcomeView.as_view(), name='welcome'),
]