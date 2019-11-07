import requests
import facebook
from pprint import pprint

FBConfig = { 'Red Alert' :
             {
                 'App Name' : 'Red Alert',
                 'App Id' : '465059364224909',
                 'App Secret' : '40abe5a8d92937cf871318410ffeea5d',
                 'Token URL' : 'https://developers.facebook.com/tools/accesstoken',
                 'App Token' : '465059364224909|jbcfzdN1Pa1JV6Z0gACVJcWUR9M',
                 'Short User Token' : 'EAAGmZBBI0P40BAFGV48CIZBFwVyGaW0uxKORTksVVphN3txtuF1ZAHJy1mfFgvFQRXCfiObSWllj5ChuuOQTHMWKVWttQWOGKsaHu8HZCBfA2sahxQvsZChft37lnqthZAdekjISeFOt8Bx26paoZAfo8ZAZBKmqZBxLF7Kfac6UsSj6C2KTxXpHnay8ZAv30BFSitiukgJAhM7QOcsY3y4bgpv'
             },
             'MyAPITestUser' :
             {
                 'App Name' : 'MyAPITestUser',
                 'App Id' : '388788568499356',
                 'App Secret' : '7a26f5adda001f1c502f3faacea86858',
                 'Token URL' : 'https://developers.facebook.com/tools/accesstoken',
                 'App Token' : '388788568499356|Uvi1C2Rgma_pnxxFZf1NBiD1w5Y',
                 'Short User Token' : 'EAAFhmeSEpJwBAN9oq8RFBkKUDkP579QDE5WrphnbDjjjnwszqapCsHCYb0fWZBcKPcQc44F8MyEZB0PZCNoBKBTN1ZB6S51V8IZB05xGJ2ZBmNXqItdWVqXWTVh9pCcAvz1KMB2AFas8yYklhkj1ZAPhHOxAudJEzYJwPai7BC9CbC7ainRjweS3BfMeYZCvZB1SvfJuBwliw9hulltFpzKuo'
             }
}


def getLongLivedUserToken(app):
    config = FBConfig[app]

    app_id = config['App Id']
    app_secret = config['App Secret']
    user_short_token = config['Short User Token']
    access_token_url = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}".format(app_id, app_secret, user_short_token)

    r = requests.get(access_token_url)

    access_token_info = r.json()
    print('--- Access Token ---')
    print(access_token_info)
    user_long_token = access_token_info['access_token']
    print('--- User Long Token ---')
    print(user_long_token)

    return user_long_token


def getGraphAPI(user_long_token):
    graph = facebook.GraphAPI(access_token=user_long_token, version='3.1')
    print('--- Graph Object Dict ---')
    print(graph.__dict__)
    return graph


def getPermanentPageTokens(graph):
    pages_data = graph.get_object("/me/accounts")
    pprint(pages_data)
    return pages_data


def getPageToken(pages_data, page_id):
    page_token = None

    for item in pages_data['data']:
        if item['id'] == page_id:
            page_token = item['access_token']
      
    print(page_token)


def tests():
    long_token = getLongLivedUserToken('Red Alert')
    graph = getGraphAPI(long_token)
    pages_data = getPermanentPageTokens(graph)
    acf_page_id = '1956513164607920'
    page_token = getPageToken(pages_data, acf_page_id)


if __name__ == '__main__':
    tests()
