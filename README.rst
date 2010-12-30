====================
django-twitter-users
====================

The django-twitter-users app is a simple, drop-in application that handles
authenticating users via the "Sign in with Twitter" service. It builds on the
django.contrib.auth app to provide a simple API for authentication.

It should take less than one hour to download this app, add it to your project,
and begin authenticating with Twitter. That begins here, with this
documentation, which should explain everything you need to know. It is
recommended that you read through this entire file.

Dependencies
------------

- python-oauth2 <https://github.com/simplegeo/python-oauth2>

Installation
------------

#. Add the ``twitter_users`` directory to your Python path.

#. Make sure that ``django.contrib.auth`` is listed in the INSTALLED_APPS list
   in ``settings.py``.

#. Add the ``twitter_users`` application to the INSTALLED_APPS list in
   ``settings.py``.

#. Add the twitter backend to the ``AUTHENTICATION_BACKENDS`` setting. By
   default, Django sets this to its own backend class. You are free to either
   add to this setting or replace it.::
   
       AUTHENTICATION_BACKENDS = (
           'twitter_users.backends.TwitterBackend',
           # Uncomment the next line if you want to also allow password auth
           #'django.contrib.auth.backends.ModelBackend',
       )

#. Configure with your desired settings.

Configuration
-------------

#. Add your consumer key and secret to ``settings.py`` after registering your
   application at <http://dev.twitter.com/apps>::

    TWITTER_KEY    = 'YOUR CONSUMER KEY'
    TWITTER_SECRET = 'YOUR CONSUMER SECRET'

#. Add URLs for authentication. You can do this by including the provided URLs.::

       urlpatterns = patterns('',
           url(r'^twitter/', include('twitter_users.urls')),
       )

   3 URLs will be provided, with names:
   
   #. ``twitter-login``: ``^login/?$``

   #. ``twitter-callback``: ``^login/callback/?$``:

   #. ``twitter-logout``: ``^logout/?$``

   Each of these URLs is connected a view of the same name in
   ``twitter_users.views`` (except the view names use underscores, not dashes).

   Otherwise, you can map your own custom URLs to the provided views. (More
   information is provided about these views below.) If you choose to provide
   your own URLs, they must be given the same names as the provided URLs above.
   
   Specifiying a callback URL is not required. If no view is named
   ``twitter-callback``, then no URL will be passed in the authentication
   request. In this case, Twitter will redirect to the default callback URL
   that's specified in your Twitter application settings.

#. Specify where users should be redirected after logging in. This can be done
   via a variety of methods, listed here in the order of precedence. After the
   processing in ``twitter_callback``, the user will be redirected.
   
   - Specify the redirect URL as part of the call to ``twitter-login``.
   
     The name of the parameter can be specified with a parameter to the
     ``twitter-login`` view (see below), but it defaults to "next". If a request
     parameter with this name is found and is valid, then upon authentication
     the user will be redirected to the specified URL.
   
   - Set ``LOGIN_REDIRECT_VIEW`` in ``settings.py``.::
     
         LOGIN_REDIRECT_VIEW = 'your-view-name'
     
     This view should take a single positional argument: the user's id.
   
   - Set ``LOGIN_REDIRECT_URL``, a standard Django setting.::
     
         LOGIN_REDIRECT_URL = '/path/to/url'
     
     Django specifies a default value for this setting, so if you don't specify
     a view or URL with one of the other methods, than this one will be used. At
     the time of this writing, the default value is ``/accounts/profile/``.

#. Specify where users should be redirected after logging out. There are several
   available options, presented here in order of precedence.
   
   - Specify the redirect URL as part of the call to ``twitter-logout``.
   
     The name of the parameter can be specified with a parameter to the
     ``twitter-logout`` view (see below), but it defaults to "next". If a
     parameter with this name is found and is valid, then after logging out, the
     user will be redirected to the specified URL.
   
   - Set ``LOGOUT_REDIRECT_VIEW`` in your settings.::
     
         LOGOUT_REDIRECT_VIEW = 'your-view-name'
     
     This view should take a single positional argument: the user's id.
   
   - Set ``LOGOUT_REDIRECT_URL``, which resembles ``LOGIN_REDIRECT_URL``, but is
     not a standard Django setting.::
     
          LOGOUT_REDIRECT_URL = '/path/to/url'
     
     The default value for this setting is ``/``.

#. Set login and logout URLs, using Django's standard ``LOGIN_URL`` and
   ``LOGOUT_URL`` settings. While authentication will work properly without
   them, some items, like the ``@login_required`` decorator will not work
   correctly.
   
   At of the time of this writing, these settings default to
   ``/accounts/login/`` and ``/accounts/logout/``.
   
   You can point these either to ``twitter-login`` and ``twitter-logout``, or to
   more generic login and logout views, depending on what user experience you
   want. (You would want a generic login page when handling multiple sign-in
   options).

#. Optionally set the format for usernames. By default, the usernames will be
   set to the users' twitter screen names. This can be changed by setting a
   variable in ``settings.py``.::
   
       TWITTER_USERS_FORMAT = '%s@twitter.com'
   
   The format takes a single string argument: the user's twitter screen name.

   This is primarily useful when using multiple authentication schemes, as a
   way to guarantee unique usernames.

Views
-----

``twitter_login(request[, redirect_field_name])``
  Redirects the user to Twitter to authenticate, resulting in a call to
  ``twitter-callback``, further processing, and a redirect to the
  post-authentication view or URL.
  
  You can specify a URL where the user should be redirected after authentication
  is complete with a request parameter. (The ``@login_required`` decorator will
  do this.) The parameter name can be specified with ``redirect_field_name``,
  but it defaults to "next". If no redirect URL is included in the request
  parameters, then redirection will occur as specified above.

``twitter_callback(request)``
  Continues processing authentication after the redirect to Twitter and
  redirects to the post-authentication view or URL.
  
  This view isn't called directly. It should only be called with a redirect from
  Twitter after authentication is complete. This is where the user will actually
  be created (if needed) and then logged in.

``twitter_logout(request[, redirect_field_name])``
  Log out the user and redirects to another page.
  
  You can specify a URL where the user should be redirected after logging out
  with a request parameter. The parameter name can be specified with
  ``redirect_field_name``, but it defaults to "next". If no redirect URL is
  included in the request parameters, then redirection will occur as specified
  above.

Notes
-----

- There is a 1-1 relationship between users and twitter accounts.

- Usernames are not guaranteed to remain static - users can change them.
  Instead, rely on user IDs, which are guaranteed to remain the same.

- Twitter usernames and user ids can be accessed through a user's TwitterInfo
  object.::
  
      from django.contrib.auth.models import User
      
      user = User.objects.get(...)
      name = user.twitter_info.name
      id   = user.twitter_info.id

- To find other Twitter users, you can use the
  ``twitter_users.models.TwitterInfo`` class.::
  
      from twitter_users.models import TwitterInfo
      
      # don't search by screen name if you can avoid it, because they're not
      # guaranteed to remain static.
      other_user = TwitterInfo.objects.get(id=other_user_twitter_id).user

- The ``token`` and ``secret`` fields on ``TwitterInfo`` objects can be used
  with the Twitter API to access the user's information.

- There's nothing special about the ``twitter-logout`` view. Any generic logout
  view will work, as long as it calls the ``logout`` function provided by
  ``django.contrib.auth``.

- The email address for user accounts created from twitter will be of the form
  ``username@twitter.com``.

Author
------

Matt Diephouse <matt@diephouse.com>

See Also
--------

<https://github.com/mdiep/django-twitter-users>

License
-------

This code is released under The BSD License.

