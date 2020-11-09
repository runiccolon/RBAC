from django.conf.urls import url
from rbac.views import role


urlpatterns = [

    url(r'^role/list/$', role.role_list, name='role_list'),
    url(r'^role/add/$', role.role_add, name='role_add'),
    url(r'^role/edit/(?P<rid>\d+)/$', role.role_edit, name='role_edit'),
]
