from django.conf.urls import url
from . import views

app_name = "pm"

urlpatterns = [
    # /music/
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^group/add$', views.GroupCreate.as_view(), name='group-add'),
    url(r'^group/edit/(?P<pk>[0-9]+)/$', views.GroupUpdate.as_view(), name='group-update'),
    url(r'^group/delete/(?P<pk>[0-9]+)/$', views.GroupDelete.as_view(), name='group-delete'),
]
