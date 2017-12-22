from django.conf.urls import url

from . import views

app_name = 'polls_djbook_tutorial'
urlpatterns = [
    # ex: /polls_djbook_tutorial/
    url(r'^$', views.Index_View.as_view(), name='index'),
    # ex: /polls_djbook_tutorial/5/
    url(r'^(?P<pk>[0-9]+)/$', views.Detail_View.as_view(), name='detail'),
    # ex: /polls_djbook_tutorial/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.Results_View.as_view(), name='results'),
    # ex: /polls_djbook_tutorial/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]