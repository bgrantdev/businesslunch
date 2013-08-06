from django.conf.urls import patterns, include, url
from businesslunch.views import HomeView, JoinView
from django.contrib.auth.views import login, logout_then_login

urlpatterns = patterns('',
                       url(
                           regex=r'^$',
                           view=HomeView.as_view(),
                           name='home'
                       ),
                       url(
                           regex=r'^/(?P<date>\d{2}-\d{2}-\d{4})$',
                           view=HomeView.as_view(),
                           name='home'
                       ),
                       url(
                           regex=r'^login$',
                           view=login,
                           kwargs={'template_name': 'login.html'},
                           name='login'
                       ),
                       url(
                           regex=r'^logout$',
                           view=logout_then_login,
                           kwargs={'login_url': '/login'},
                           name='logout'
                       ),
                       url(
                           regex=r'^join/(?P<opt_in_id>\d+$)',
                           view=JoinView.as_view(),
                           name='join'
                       ),
)
