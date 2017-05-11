'''
DO NOT MODIFY THIS FILE!
Created by Justin Boucher
jboucher@splunk.com
'''

from os import environ
import base64
import datetime as dt
import ConfigParser
import cherrypy, threading
import requests, urllib
import json

# Setup Splunk Environment
APPNAME = 'test_app'
CONFIG = 'appconfig.conf'
SPLUNK_HOME = environ['SPLUNK_HOME']
TOKEN_CONFIG = '/bin/token_settings.txt'

tokenfile = SPLUNK_HOME + '/etc/apps/' + APPNAME + TOKEN_CONFIG

parser = ConfigParser.SafeConfigParser()


class APIFramework():

    def __init__(self):
        pass

    # All information must be as on the API configuration page for the app you are connecting to.
    # Load Settings
    parser.read(SPLUNK_HOME + '/etc/apps/' + APPNAME + '/local/' + CONFIG)
    if parser.has_section('Authentication'):
        pass
    else:
        parser.read(SPLUNK_HOME + '/etc/apps/' + APPNAME + '/default/' + CONFIG)

    CLIENT_ID = parser.get('Authentication', 'C_KEY')
    CLIENT_SECRET = parser.get('Authentication', 'C_SECRET')
    REDIRECT_URI  = parser.get('Authentication', 'REDIRECT_URI')

    # Decide which information the API should have access to.
    # Enter scopes as tuple with commas in between
    SCOPES = parser.get('AppServer', 'SCOPES')
    API_SCOPES = tuple(SCOPES.split(','))

    # These settings should probably not be changed.
    API_SERVER = parser.get('AppServer', 'API_SERVER')
    AUTHORIZE_URL = parser.get('AppServer', 'AUTHORIZE_URL')
    TOKEN_URL = parser.get('AppServer', 'TOKEN_URL')

    def get_authorization_uri(self):

        # Parameters for authorization, make sure to select
        params = {
            'client_id': self.CLIENT_ID,
            'response_type': 'code',
            'scope': ' '.join(self.API_SCOPES),
            'redirect_uri': self.REDIRECT_URI
        }

        # Encode parameters and construct authorization url to be returned to user.
        urlparams = urllib.urlencode(params)
        return "%s?%s" % (self.AUTHORIZE_URL, urlparams)

        # Tokes are requested based on access code. Access code must be fresh (10 minutes)

    def get_access_token(self, access_code):

        # Construct the authentication header
        auth_header = base64.b64encode(self.CLIENT_ID + ':' + self.CLIENT_SECRET)
        headers = {
            'Authorization': 'Basic %s' % auth_header,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Parameters for requesting tokens (auth + refresh)
        params = {
            'code': access_code,
            'grant_type': 'authorization_code',
            'client_id': self.CLIENT_ID,
            'redirect_uri': self.REDIRECT_URI
        }

        # Place request
        resp = requests.post(self.TOKEN_URL, data=params, headers=headers)
        status_code = resp.status_code
        resp = resp.json()

        if status_code != 200:
            raise Exception("Something went wrong exchanging code for token (%s): %s" % (
                resp['errors'][0]['errorType'], resp['errors'][0]['message']))

        # Strip the goodies
        token = dict()
        token['access_token'] = resp['access_token']
        token['refresh_token'] = resp['refresh_token']

        return token

        # Get new tokens based if authentication token is expired

    def ref_access_token(self, token):

        # Construct the authentication header
        auth_header = base64.b64encode(self.CLIENT_ID + ':' + self.CLIENT_SECRET)
        headers = {
            'Authorization': 'Basic %s' % auth_header,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Set up parameters for refresh request
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': token['refresh_token']
        }

        # Place request
        resp = requests.post(self.TOKEN_URL, data=params, headers=headers)

        status_code = resp.status_code
        resp = resp.json()

        if status_code != 200:
            raise Exception("Something went wrong refreshing (%s): %s" % (
            resp['errors'][0]['errorType'], resp['errors'][0]['message']))

        # Distil
        token['access_token'] = resp['access_token']
        token['refresh_token'] = resp['refresh_token']

        return token

        # Place api call to retrieve data

    def api_call(self, token, api_call=parser.get('AppServer', 'SAMPLE_CALL')):

        headers = {
            'Authorization': 'Bearer %s' % token['access_token']
        }

        final_url = self.API_SERVER + api_call

        resp = requests.get(final_url, headers=headers)

        status_code = resp.status_code

        resp = resp.json()
        resp['token'] = token

        if status_code == 200:
            return resp
        elif status_code == 401:
            # print "The access token you provided has been expired let me refresh that for you."
            # Refresh the access token with the refresh token if expired. Access tokens should be good for 1 hour.
            token = self.ref_access_token(token)
            json.dump(token, open(tokenfile, 'w'))
            self.api_call(token, api_call)
        else:
            raise Exception("Something went wrong requesting (%s): %s" % (
            resp['errors'][0]['errorType'], resp['errors'][0]['message']))

            # CherryPy to facilitate user interaction

    @cherrypy.expose
    def index(self, code=None):
        if code:
            def query():
                yield "Copy this code into the access_generator utility: "
                yield cherrypy.request.params.get('code', None)
        self._shutdown_cherrypy()
        return query()

    index.exposed = True

    def _shutdown_cherrypy(self):
        """ Shutdown cherrypy in one second, if it's running """
        if cherrypy.engine.state == cherrypy.engine.states.STARTED:
            threading.Timer(1, cherrypy.engine.exit).start()

    def read_token(self):
        try:
            token = json.load(open(tokenfile))
        except IOError:
            print "Error retrieving access token. Please rerun provided access_generator.py!"
            auth_url = APIFramework.get_authorization_uri()
            print "Please visit the link below and approve the app:\n %s" % auth_url
            # Set the access code that is part of the arguments of the callback URL the app redirects to.
            access_code = raw_input("Please enter code (from the URL you were redirected to): ")
            # Use the temporary access code to obtain a more permanent pair of tokens
            token = APIFramework.get_access_token(access_code)
            # Save the token to a file
            json.dump(token, open(tokenfile, 'w'))
        return token

    def time_series(self, endpoint):
        if parser.has_section(endpoint):
            pass
        else:
            parser.read(SPLUNK_HOME + '/etc/apps/' + APPNAME + '/default/' + CONFIG)

        date_interval = parser.get(endpoint, 'DATE_INTERVAL')
        time_interval = parser.get(endpoint, 'TIME_INTERVAL')
        time_delay = parser.get(endpoint, 'TIME_DELAY')

        # Create start time and end time for api call
        delay = int(time_delay)
        now = dt.datetime.now()
        delta = dt.timedelta(minutes=delay)
        t = now.time()
        end_time = (t.strftime('%H:%M'))

        # Subtract x minutes from start time to provide end time
        start_time = ((dt.datetime.combine(dt.date(1, 1, 1), t) + delta).time().strftime('%H:%M'))

        time_series = {'DATE': date_interval, 'TIME': time_interval, 'START': start_time, 'END': end_time}

        return time_series
