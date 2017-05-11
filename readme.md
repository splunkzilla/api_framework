# API Call Scripting Framework for Splunk

**Description:** Support OAuth2 API calls for custom application scripts and TA's in Splunk. Contains sourcefiles, but **needs editing before** running.

**Author:** Justin Boucher.

*__NOTE:__ Uses customized version of OAuth Scripting, and does not use the python OAuth generator to reduce number of dependencies*

## Installation Instructions

### Preparation
Before using this framework, copy the files into your app in `$SPLUNK_HOME/etc/apps/<your_app_name>`. Do not restart Splunk yet. We will need to configure the files before restarting Splunk. 

### Configure the Framework
Using your terminal, run `python setup.py` to begin the configuration. Setup will attempt to configure the entire app by asking a few questions. Below are definitions of the questions asked in `setup.py`

* ###### Name of app ######
     Name of the app as it appears in `$SPLUNK_HOME/etc/apps`. This will configure the proper directory names for the configuration and modify the app name in the required files. *__NOTE:__* This framework contains an `app.conf` file, and this file will need to be modified outside of `setup.py` or replaced by your apps `app.conf` file.
* ###### Name of API Server ######
     Name of the API server you are connecting. This framework already adds the https:// to the url, and it is not required for this field. For example, if my api is located at https://api.myapp.com; then input `api.myapp.com` in the field.
* ###### Name of WWW Server ######
     Name of the website you are connecting. This framework already adds the http:// to the url, and it is not required for this field. For example, if my website is located at http://www.myapp.com; then input `www.myapp.com` in the field.
* ###### Name of Authorization URL ######
     Name of the authorization url for the API. This framework already adds the name of the WWW server to the url, and it is not required for this field. For example, if my authorization url is located at http://www.myapp.com/oauth2/authorize; then input `/oauth2/authorize` in the field. Please check your API's documentation for this information.
* ###### Name of Token URL ######
     Name of the token url for the API. This field facilitates refreshing tokens in the framework to continuously receive data from the API. This framework already adds the name of the WWW server to the url, and it is not required for this field. For example, if my token url is located at http://api.myapp.com/oauth2/token; then input `/oauth2/token` in the field. Please check your API's documentation for this information.
* ###### Requested Scopes ######
    Scopes are the permissions you are requesting access to in your API. These are also called app permissions in many APIs. These values need to be comma separated. For example, if the API has the scopes or permissions of profile and activity, then input `profile,activity` in the field.

*TODO: Finish writing this README!*