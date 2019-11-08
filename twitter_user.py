import os.path
import tweepy

import pylib.exceptions

class TwitterUserException(pylib.exceptions.BasicException):
    def __init__(self, errmsg):
        super().__init__(errmsg)


class TwitterUser:

    def __init__(self,
                 consumer_key,
                 consumer_secret,
                 access_token=None,
                 access_token_secret=None,
                 callback_url=None):

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.callback_url = callback_url
        self.api = None
        self.redirect_url = None

        # Start authentication
        self.auth = tweepy.OAuthHandler(self.consumer_key,
                                        self.consumer_secret,
                                        self.callback_url)
        if self.has_credentials():
            self.set_credentials()


    @property
    def request_token(self):
        return self.auth.request_token['oauth_token']


    def get_authorization_url(self):
        try:
            self.redirect_url = self.auth.get_authorization_url()
        except tweepy.TweepError:
            raise TwitterUserException('Error! Failed to get redirect url.')


    def get_credentials(self, verifier):
        self.auth.request_token = { 'oauth_token' : self.request_token,
                                    'oauth_token_secret' : verifier }
        # Retrieve access token and access token secret and store
        # then in auth.access_token and auth.access_token_secret
        self.auth.get_access_token(verifier)
        self.access_token = self.auth.access_token
        self.access_token_secret = self.auth.access_token_secret


    def has_credentials(self):
        return self.access_token and self.access_token_secret


    def set_api(self):
        self.api = tweepy.API(self.auth)


    def set_credentials(self, access_token=None, access_token_secret=None):
        # authentication of access token and secret 
        if access_token:
            self.access_token = access_token
        if access_token_secret:
            self.access_token_secret = access_token_secret
        self.auth.set_access_token(self.access_token, self.access_token_secret)


    def tweet(self, text):
        self.api.update_status(text)


#--- Tests

import webbrowser
from datetime import datetime

def tweet(tu, text):
    text = '[TEST] ' + text + ' --> ' + datetime.now().isoformat()
    tu.api.update_status(text)
    return text

def test():

    cfg = {
        'callback_url' : 'http://localhost:2727/twitter_oauth_callback',
        'api_key' : 'yhxbp8Nx8mthDpQw6kMry3EMM',
        'api_security_key' : '2uz6VVdXGrRHxD8coQHJ0GXlOg8pyezE5VgCyAwq1zHToM101R',
        'user' : 'testuser@example.com',
        'access_token' : None,
        'access_token_secret' : None
    }

    print('For OAuth process see: https://oauth.net/core/diagram.png')

    from redalert.src.ucreds import UCredsDb

    tu = TwitterUser(consumer_key=cfg['api_key'],
                     consumer_secret=cfg['api_security_key'],
                     access_token=cfg['access_token'],
                     access_token_secret=cfg['access_token_secret'],
                     callback_url=None)
                   # cfg['callback_url'] FIXME! Why does specifying callback url does not work?
                     
    if tu.has_credentials():
        print('Credentials obtained')
        
    else: # Acquire access token
        print('Acquiring credentials...')

        #-------
        # 1) Get a request token from twitter
        # 2) Redirect user to twitter.com to authorize our application
        # 3) If using a callback, twitter will redirect the user to us.
        #    Otherwise the user must manually supply us with the verifier code.
        # 4) Exchange the authorized request token for an access token.
        #-------
        
        # Get a request token and save it
        tu.get_authorization_url()

        #-------
        # This call requests the token from twitter and returns to us the
        # authorization URL where the user must be redirect to authorize us.
        # Now if this is a desktop application we can just hang onto our
        # OAuthHandler instance until the user returns back. In a web
        # application we will be using a callback request. So we must store
        # the request token in the session since we will need it inside the
        # callback URL request. Here is a pseudo example of storing the request
        # token in a session:
        #-------

        webbrowser.open(tu.redirect_url)
        verifier = input('Enter verifier: ')

        # The final step is exchanging the request token for an access token.
        # The access token is the “key” for opening the Twitter API treasure box.

        tu.get_credentials(verifier)

    tu.set_api()
    return

    tweet(tu,
          '''
          This is a test! We are working on developing 
          'an application to notify Twitter users whenever
          rockets are fired into Israel
          '''
    )


if __name__ == '__main__':
    try:
        test()
    except tweepy.TweepError as e:
        print('Error! Failed to get access token!')
        print(e)
