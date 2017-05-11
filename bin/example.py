'''
This example shows a simple print of data from the API to Splunk.
Change the below API_CALL variable to match your APIs documentation.
The result should print the API response contents to the screen.

This is the default functionality, and can be used for almost all API calls.
'''
######### BEGIN DO NOT MODIFY ############
import json
from bin.lib import api_framework

# import requests.packages.urllib3
# requests.packages.urllib3.disable_warnings()

api = api_framework.APIFramework()

# Try to read existing token pair
token = api.read_token()

########## END DO NOT MODIFY ##########

### BEGIN API SPECIFIC MODIFICATION ###

# Modify this variable for your specific API
API_CALL = '/1/user/-/profile.json'

# Send data query request to the API
query = api.api_call(token, API_CALL)

# Get response and format for ingestion in Splunk
response = json.dumps(query)

'''
Add your custom actions here for the response
variable.
'''

# send to STDOUT for Splunk ingestion
print response

######### END EXAMPLE ###########