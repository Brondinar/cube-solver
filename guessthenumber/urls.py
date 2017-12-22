from django.conf.urls import url

from . import views

app_name = 'guessthenumber'
urlpatterns = [
    url(r'^$', views.game_index, name='index'),
    url(r'^game/$', views.game_process, name='game_process'),
]