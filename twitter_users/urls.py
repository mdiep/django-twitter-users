
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('twitter_users.views',
    url(r'^login/?$',           'twitter_login',    name='twitter-login'),
    url(r'^login/callback/?$',  'twitter_callback', name='twitter-callback'),
    url(r'^logout/?$',          'twitter_logout',   name='twitter-logout'),
)

