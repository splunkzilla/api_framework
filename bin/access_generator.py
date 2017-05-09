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

# Setup Splunk Environment
APPNAME = '<APPNAME>'
CONFIG = '/bin/user_settings.txt'
SPLUNK_HOME = os.environ['SPLUNK_HOME']

tokenfile = SPLUNK_HOME + '/etc/apps/' + APPNAME + CONFIG

api = api_framework.APIFramework()

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
response = api.api_call(token, '/1/user/-/profile.json')

# Token is part of the response. Note that the token pair can change when a refresh is necessary.
# So we replace the current token with the response one and save it.
token = response['token']
json.dump(token, open(tokenfile, 'w'))

# Do something with the response
print "Welcome %s, your %s account is now connected!" % (response['user']['displayName'], APPNAME)
