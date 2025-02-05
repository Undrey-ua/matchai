from authlib.integrations.starlette_client import OAuth

oauth = OAuth()

# Facebook
oauth.register(
    name='facebook',
    client_id='YOUR_FACEBOOK_CLIENT_ID',
    client_secret='YOUR_FACEBOOK_CLIENT_SECRET',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    access_token_params=None,
    authorize_url='https://www.facebook.com/dialog/oauth',
    authorize_params=None,
    api_base_url='https://graph.facebook.com/',
    client_kwargs={'scope': 'email user_likes user_posts'}
)

# Twitter
oauth.register(
    name='twitter',
    client_id='YOUR_TWITTER_CLIENT_ID',
    client_secret='YOUR_TWITTER_CLIENT_SECRET',
    access_token_url='https://api.twitter.com/oauth/access_token',
    access_token_params=None,
    authorize_url='https://api.twitter.com/oauth/authenticate',
    authorize_params=None,
    api_base_url='https://api.twitter.com/1.1/',
    client_kwargs={'scope': 'tweet.read users.read like.read'}
) 