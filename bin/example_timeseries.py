'''
This example shows a simple print of data from the API to Splunk
using specific date and time mappings. Please note that appconfig.conf
will need to be modified in order to change the date and time info.
Change the below API_CALL variable to match your APIs documentation.
The result should print the API response contents to the screen.

Time Series information is used to reduce
the amount of data required for Splunk to ingest.
This will reduce license usage and help to ensure
duplicate results are not ingested in your app.
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

# API Call to perform before the date and time
API_CALL = '/1/user/-/activities/date/today/'

# Get time series information.
time_series = api.time_series('TimeSeries1') # Must match stanza name in appconfig.conf

# Get time series intervals from appconfig.conf
date_interval = time_series['DATE']
time_interval = time_series['TIME']
start_time = time_series['START']
end_time = time_series['END']

# Concatenate query string to include time series information
api_str = API_CALL + date_interval + '/' + time_interval + '/time/' + start_time + '/' + end_time + '.json'

# Send data request to API
query = api.api_call(token, api_str)

'''
Add your custom actions here for the response
variable.
'''

# send to STDOUT for Splunk ingestion
print response

######### END EXAMPLE ###########