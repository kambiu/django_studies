from django.conf.urls import url
from . import views

app_name = "music"

urlpatterns = [
    # /music/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /music/712/ extract the alubm id to the variable --> album_id

    # ?P <-- Pattern<variable_name>
    # see views.py def detail(request, album_id)
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # /music/<album_id>/favorite/
    # url(r'^(?P<album_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
]
