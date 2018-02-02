from django.conf.urls import url

from . import views

app_name = 'cube_solver'
urlpatterns = [
    url(r'^$', views.cube_index, name='index'),
    url(r'^solve/$', views.cube_solve, name='solve'),
]