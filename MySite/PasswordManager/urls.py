from django.conf.urls import url
from . import views

app_name = "pm"

urlpatterns = [
    # /main/
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_page, name='login'),
    url(r'^logout/$', views.logout_request, name='logout'),
    url(r'^login/request/$', views.login_request, name='login-request'),
    url(r'^main/$', views.GroupListView.as_view(), name='group-list'),
    # group
    url(r'^(?P<pk>[0-9]+)/$', views.GroupDetailView.as_view(), name='group-detail'),
    url(r'^group/add$', views.GroupCreate.as_view(), name='group-add'),
    url(r'^group/edit/(?P<pk>[0-9]+)/$', views.GroupUpdate.as_view(), name='group-update'),
    url(r'^group/delete/(?P<pk>[0-9]+)/$', views.GroupDelete.as_view(), name='group-delete'),
    url(r'^token/$', views.token, name='get-token'),
    # pw account
    url(r'^account/add$', views.account_create, name='account-create'),
    url(r'^account/update/(?P<account_id>[0-9]+)/$', views.account_update, name='account-update'),
    url(r'^account/$', views.account_details, name='account-details'),
    # change key
    url(r'^key/$', views.change_key, name='user-key'),
    # testing
    url(r'^test/$', views.test, name='test'),

]
