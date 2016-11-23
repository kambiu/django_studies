from django.conf.urls import url
from . import views

app_name = "pm"

urlpatterns = [
    # /music/
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.GroupDetailView.as_view(), name='group-detail'),

    url(r'^group/add$', views.GroupCreate.as_view(), name='group-add'),
    url(r'^group/edit/(?P<pk>[0-9]+)/$', views.GroupUpdate.as_view(), name='group-update'),
    url(r'^group/delete/(?P<pk>[0-9]+)/$', views.GroupDelete.as_view(), name='group-delete'),
    url(r'^token/$', views.token, name='get-token'),
    url(r'^account/add$', views.account_create, name='account-add'),
]
