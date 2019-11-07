from requests_oauthlib import OAuth1Session
from pprint import pprint

class OAuth:

    def __init__(self,
                 consumer_key,
                 consumer_secret):

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = None
        self.access_token_secret = None
        self.resource_owner_key = None
        self.resource_owner_secret = None
        self.access_token_list = None
        self.user_data_json = None


    def __str__(self):
        s = ''.join(('Consumer Key        : %s\n' % self.consumer_key,
                     'Consumer Secret     : %s\n' % self.consumer_secret,
                     'Access Token        : %s\n' % self.access_token,
                     'Access Token Secret : %s' % self.access_token_secret))
        return s
        

    def get_resource_token(self):

        #create an object of OAuth1Session
        request_token = OAuth1Session(client_key=self.consumer_key,
                                      client_secret=self.consumer_secret)

        # twitter endpoint to get request token
        url = 'https://api.twitter.com/oauth/request_token'
        # get request_token_key, request_token_secret and other details
        print('[A]: Request REQUEST TOKEN at %s (send consumer_key, consumer_secret)' % url)
        data = request_token.get(url)

        # split the string to get relevant data 
        data_token = str.split(data.text, '&')
        ro_key = str.split(data_token[0], '=')
        ro_secret = str.split(data_token[1], '=')
        self.resource_owner_key = ro_key[1]
        self.resource_owner_secret = ro_secret[1]

        print('[B]: Received REQUEST TOKEN %s' % data)
        print('\ttoken = %s, secret = %s)' % (self.resource_owner_key,
                                              self.resource_owner_secret))


    def get_access_token(self, verifier):
        oauth_token = OAuth1Session(client_key=self.consumer_key,
                                    client_secret=self.consumer_secret,
                                    resource_owner_key=self.resource_owner_key,
                                    resource_owner_secret=self.resource_owner_secret)
        url = 'https://api.twitter.com/oauth/access_token'
        data = {"oauth_verifier": verifier}
   
        print('[E]: Request ACCESS TOKEN')

        access_token_data = oauth_token.post(url, data=data)

        print('[F]; Receive ACCESS TOKEN')

        self.access_token_list = str.split(access_token_data.text, '&')


    def get_user_data(self):
        access_token_key = str.split(self.access_token_list[0], '=')
        access_token_secret = str.split(self.access_token_list[1], '=')
        access_token_name = str.split(self.access_token_list[3], '=')
        access_token_id = str.split(self.access_token_list[2], '=')
        key = access_token_key[1]
        secret = access_token_secret[1]
        name = access_token_name[1]
        id = access_token_id[1]

        oauth_user = OAuth1Session(client_key=self.consumer_key,
                                   client_secret=self.consumer_secret,
                                   resource_owner_key=key,
                                   resource_owner_secret=secret)
        url_user = 'https://api.twitter.com/1.1/account/verify_credentials.json'
        params = {"include_email": 'true'}
        user_data = oauth_user.get(url_user, params=params)
        self.user_data_json = user_data.json()


    def test(self):

        self.get_resource_token()

        print('[C]: Direct user to service provider to get ACCESS TOKEN -- for now this is a manual process')
        print('Paste the following string into your browser:')
        print('https://api.twitter.com/oauth/authenticate?oauth_token=%s' % self.resource_owner_key)
        print('Twitter now redirects to your webserver. Go to the log and get the')
        print('access token string and paste it below')

        ats = input('Access Token String: ')
        print('[D]: Received Access Token')
        atsparams = ats.split('&')
        pprint(atsparams)
        auth_token = atsparams[0].split('=')[1]
        print('auth_token = [%s]' % auth_token)
        verifier = atsparams[1].split('=')[1]
        print('verifier = [%s]' % verifier)

        self.get_access_token(verifier)

        print('\nAccess Token List:')
        pprint(self.access_token_list)
        access_token = self.access_token_list[0]
        access_token_secret = self.access_token_list[1]

        self.get_user_data()

        print('\nUser Profile Data:')
        pprint(self.user_data_json)
