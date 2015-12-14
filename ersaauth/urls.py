from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^login/$', views.login, name='login'),
    #url(r'^logout/$', views.logout, name='logout'),
    #url(r'^password_change/$', views.password_change, name='password_change'),
    #url(r'^password_change/done/$', views.password_change_done, name='password_change_done'),
    url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^password_reset/sent/$', views.password_reset_link_sent, name='password_reset_link_sent'),
    url(r'^password_reset/confirm/(?P<token>.+)/$',views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^password_reset/complete/$', views.password_reset_complete, name='password_reset_complete'),
]
