from django.conf.urls import url
from . import views

urlpatterns = [
    # /music/
    url(r'^$', views.index, name='index'),

    # /music/712/ extract the alubm id to the variable --> album_id

    # ?P <-- Pattern<variable_name>
    # see views.py def detail(request, album_id)
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
]
