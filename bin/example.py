import api_framework, json
# import requests.packages.urllib3
# requests.packages.urllib3.disable_warnings()

api = api_framework.APIFramework()

# Try to read existing token pair
token = api.read_token()

# Send data request to Fitbit
summary = api.api_call(token, '/1/user/-/profile.json')

# Get response and send to STDOUT for Splunk ingestion
summary = json.dumps(summary)

print summary
