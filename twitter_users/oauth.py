
import oauth2
import urllib

from twitter_users import settings

# not sure why this is necessary, but oauth2 does this, so I'm following its lead
try:
    from urlparse import parse_qs, parse_qsl
except ImportError:
    from cgi import parse_qs, parse_qsl

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL  = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'

class Consumer(oauth2.Consumer):
    pass

class Token(object):
    def __init__(self, consumer):
        self.consumer = consumer
    
    def _get_token(self, url, token=None, method='POST', **parameters):
        client            = oauth2.Client(self.consumer, token)
        response, content = client.request(url,
            method  = method,
            body    = urllib.urlencode(parameters)
        )
        
        if response['status'] != '200':
            return None;
        
        return content

class RequestToken(Token):
    def __init__(self, consumer, callback_url=None):
        super(RequestToken, self).__init__(consumer)
        
        parameters = {}
        if callback_url is not None:
            parameters['oauth_callback'] = callback_url
        
        token_content = self._get_token(REQUEST_TOKEN_URL, **parameters)
        self.token    = oauth2.Token.from_string(token_content)
    
    @property
    def authorization_url(self):
        request = oauth2.Request.from_consumer_and_token(
            self.consumer,
            self.token,
            http_url = AUTHORIZATION_URL
        )
        request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)
        return request.to_url()

class AccessToken(Token):
    def __init__(self, consumer, oauth_token, oauth_verifier):
        super(AccessToken, self).__init__(consumer)
        
        # parse the access token by hand to get access to the additional
        # parameters that Twitter passes back, like the user id and screen name
        token_content = self._get_token(ACCESS_TOKEN_URL, oauth_token=oauth_token, oauth_verifier=oauth_verifier)
        self.params   = parse_qs(token_content)
    
    @property
    def token(self):
        return self.params['oauth_token'][0]
    
    @property
    def secret(self):
        return self.params['oauth_token_secret'][0]
    
    @property
    def user_id(self):
        return self.params['user_id'][0]
    
    @property
    def username(self):
        return self.params['screen_name'][0]
