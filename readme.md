# API Call Scripting Framework for Splunk

**Description:** Support OAuth2 API calls for custom application scripts and TA's in Splunk. Contains sourcefiles, but **needs editing before** running.

**Author:** Justin Boucher.

*__NOTE:__ Uses customized version of OAuth Scripting, and does not use the python OAuth generator to reduce number of dependencies*

## Installation Instructions

### Preparation
Before using this framework, copy the files into your app in `$SPLUNK_HOME/etc/apps/<your_app_name>`. Do not restart Splunk yet. We will need to configure the files before restarting Splunk. 

### Configure the Framework
Using your terminal, run `python setup.py` to begin the configuration. Setup will attempt to configure the entire app by asking a few questions. Below are definitions of the questions asked in `setup.py`:

* ###### Name of app ######
     Name of the app as it appears in `$SPLUNK_HOME/etc/apps`. This will configure the proper directory names for the configuration and modify the app name in the required files. *__NOTE:__* This framework contains an `app.conf` file, and this file will need to be modified outside of `setup.py` or replaced by your apps `app.conf` file.
* ###### Name of API Server ######
     Name of the API server you are connecting. For example, if my api is located at https://api.myapp.com; then input `https://api.myapp.com` in the field. Please check your API's documentation for this information.
* ###### Name of Authorization URL ######
     Name of the authorization url for the API. For example, if my authorization url is located at http://www.myapp.com/oauth2/authorize; then input `http://www.myapp.com/oauth2/authorize` in the field. Please check your API's documentation for this information.
* ###### Name of Token URL ######
     Name of the token url for the API. This field facilitates refreshing tokens in the framework to continuously receive data from the API. For example, if my token url is located at http://api.myapp.com/oauth2/token; then input `http://api.myapp.com/oauth2/token` in the field. Please check your API's documentation for this information.
* ###### Requested Scopes ######
    Scopes are the permissions you are requesting access to in your API. These are also called app permissions in many APIs. These values need to be comma separated. For example, if the API has the scopes or permissions of profile and activity, then input `profile,activity` in the field.
* ###### Sample Call ######
    Following you API's documentation, identify a sample API call to perform during the access generation phase of the configuration. This will check the ability of the framework's ability to properly access the API data. For example, MyApp documentation states that /user/1/-/profile.json will return user profile information for the user. In this case input `/user/1/-/profile.json` into the field.*__NOTE:__* Not all API's will provide a stop error code. Some response errors will be in a format that is not checked in the `access_generator.py` script. Please review the output of the response to confirm that the data is accessible.
* ###### Client Key ######
    Following you API's documentation, input your Client Key provided during your API setup phase. Example: `12732483432`. 
* ###### Secret Key ######
    Following you API's documentation, input your Secret Key provided during your API setup phase. Example: `9sd8sd9a8da9s8das0d98as`. 
* ###### Callback URL ######
    This url is used to create the refresh tokens and allow continuous access to the API data in your scripts. This process is handled by the framework, but needs to be added exactly how it is configured in your API. Recommend using the standard `http://127.0.0.1:8080`, and updating your API accordingly. You may use a different port or system, but ensure that you do not use any port already used by Splunk. 

Once you have answered these questions, the setup will prompt you to determine whether or not you want to write these changes to the `appconfig.conf` file. Type `y [enter]` to confirm the changes. Proceed to the next part of this installation.

### Getting API Tokens
Setup will prompt you to run the `access_generator.py` script. If your configuration is correct, you should be able to run this without any problems. The access generator will contact the API using your settings, then return an access key and refresh token. These token will be stored in `$SPLUNK_HOME/etc/apps/<your_app_name>/bin/lib/token_configs.txt` for future use in your scripts. As the framework runs, your new tokens will also be overwritten in this file. The `access_generator` does require some initial information, however.

The `access_generator` will spawn a webbrowser that is pointed to your API. Once you have accepted the scope/permissions for the account, your API should return an access token. Copy this access token from the browser window, and paste this token back into the terminal when prompted. Once the code has been confirmed, it will run the `SAMPLE CALL` you created during the configuration steps. 

Review the response, and determine if your call worked properly (see note on sample call for more info). This completes the setup process. Now restart Splunk and everything should be kosher.

## Creating Scripts ##
This section will attempt to guide you through the process of creating your first script. But I have to write it first.

*TODO: Finish writing this README!*