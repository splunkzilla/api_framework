'''
access_generator.py
Needed to develop initial access tokens for script use.
Currently in Beta version. Email me to get instructions on
usage. I need to automate process still. - JB
'''

import api_framework
import json
import os
import cherrypy, webbrowser
import ConfigParser

# Setup Splunk Environment
APPNAME = 'test_app'
PARSER_CONFIG = 'appconfig.conf'
CONFIG = '/bin/token_settings.txt'
SPLUNK_HOME = os.environ['SPLUNK_HOME']

parser = ConfigParser.SafeConfigParser()

tokenfile = SPLUNK_HOME + '/etc/apps/' + APPNAME + CONFIG

api = api_framework.APIFramework()

# All information must be as on the API configuration page for the app you are connecting to.
    # Load Settings
parser.read(SPLUNK_HOME + '/etc/apps/' + APPNAME + '/local/' + PARSER_CONFIG)
if parser.has_section('Authentication'):
    pass
else:
    parser.read(SPLUNK_HOME + '/etc/apps/' + APPNAME + '/default/' + PARSER_CONFIG)

# Try to read existing token pair
try:
    token = json.load(open(tokenfile))
except IOError:
    # If not generate a new file
    # Get the authorization URL for user to complete in browser.
    auth_url = api.get_authorization_uri()
    webbrowser.open(auth_url)
    cherrypy.quickstart(api)
    # Set the access code that is part of the arguments of the callback URL FitBit redirects to.
    access_code = raw_input("Please enter code (from the URL you were redirected to): ")
    # Use the temporary access code to obtain a more permanent pair of tokens
    token = api.get_access_token(access_code)
    # Save the token to a file
    json.dump(token, open(tokenfile, 'w'))

# Sample API call
SAMPLE_CALL = parser.get('AppServer', 'SAMPLE_CALL')
response = api.api_call(token, SAMPLE_CALL)

# Token is part of the response. Note that the token pair can change when a refresh is necessary.
# So we replace the current token with the response one and save it.
token = response['token']
try:
    json.dump(token, open(tokenfile, 'w'))
    # Do something with the response
    print "\nHere was the response:"
    print response
    print "\n\nCongrats your %s account is now connected! Look above for the response.\n" % APPNAME
except:
    print "There was an error retrieving the sample data call. \
    Please review the %s configuration and your API documentation." % APPNAME
