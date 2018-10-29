from django.conf.urls import url

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.cube_index, name='index'),
    url(r'^solve/$', views.cube_solve, name='solve'),
]