
from django.conf import settings

# Required
KEY                  = settings.TWITTER_KEY
SECRET               = settings.TWITTER_SECRET

# Optional
LOGIN_REDIRECT_VIEW  = getattr(settings, 'LOGIN_REDIRECT_VIEW', None)
LOGIN_REDIRECT_URL   = settings.LOGIN_REDIRECT_URL # Django supplies a default value

LOGOUT_REDIRECT_VIEW = getattr(settings, 'LOGOUT_REDIRECT_VIEW', None)
LOGOUT_REDIRECT_URL  = getattr(settings, 'LOGOUT_REDIRECT_URL',  '/')

PROFILE_MODULE       = getattr(settings, 'AUTH_PROFILE_MODULE',
                                         'twitter_users.models.UserProfile')
USERS_FORMAT         = getattr(settings, 'TWITTER_USERS_FORMAT', '%s')

