import sys
from os import walk, path, system
from distutils.util import strtobool
import site


def user_yes_no_query(question):
    '''
    Asks yes or no question and returns True or False
    :param question:
    :return: True/False
    '''
    sys.stdout.write('%s [y/n]\n' % question)
    while True:
        try:
            return strtobool(raw_input().lower())
        except ValueError:
            sys.stdout.write('Please respond with \'y\' or \'n\'.\n')


def inplace_change(filename, old_string, new_string):
    '''
    Takes filename object, the current string and the string
    to replace. Does this inline so the file doesn't have to
    be opened twice.

    :param filename:
    :param old_string:
    :param new_string:
    :return: none
    '''
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if old_string not in s:
            print '"{old_string}" not found in {filename}.'.format(**locals())
            return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        print 'Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals())
        s = s.replace(old_string, new_string)
        f.write(s)


def get_filepaths(directory):
    '''
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).

    :param directory:
    :return:
    '''
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths

'''
This app requires two python modules that don't come standard
in Splunk. THese modules are requests and cherrypy. The app will
attempt to install pip to assist in the installation of these modules.
'''
print 'Checking for Prereqs...'

try:
    import pip
except ImportError:
    print "installing pip"
    cmd = "sudo easy_install pip"
    system(cmd)
    reload(site)

try:
    import requests
except ImportError:
    print "no lib requests"
    import pip
    cmd = "pip install requests"
    print "Requests package is missing\nInstalling now..."
    system(cmd)
    reload(site)

try:
    import cherrypy
except ImportError:
    print "no lib requests"
    import pip

    cmd = "pip install cherrypy"
    print "cherrypy package is missing\nInstalling now..."
    system(cmd)
    reload(site)

print '\nAll modules installed!\n'

# Change app_name in all files to the current app_name
APP_NAME = raw_input("Enter the name of the app as it will\nappear in the /etc/apps directory: ")
print 'Making app changes\n'

paths = get_filepaths('.')

for filename in paths:
    inplace_change(filename, 'test_app', APP_NAME)

config_api = user_yes_no_query('\nDo you want to configure the API now?')

if config_api == True:
    API_SERVER =  raw_input("\nEnter the name of the API server without the https://\n[example: api.myapp.com]: ")
    WWW_SERVER = raw_input("\nEnter the name of the WWW server without the https://\n[example: www.myapp.com]: ")
    AUTHORIZE_URL = raw_input("\nEnter the name of the Authorization URL with slashes[/]\n[example: /oauth2/authorize]: ")
    TOKEN_URL = raw_input("\nEnter the name of the Token URL with slashes[/]\n[example: /oauth2/token]: ")
    SCOPES = raw_input("\nEnter the name of the Available Scopes with comma between\n[example: profile,activity]: ")
    SAMPLE_CALL = raw_input("\nEnter a sample API call for testing\n[example: /1/user/-/profile.json]: ")
    C_KEY = raw_input("\nEnter your Client Key\n[example: 12353465754]: ")
    C_SECRET = raw_input("\nEnter your Client Secret Key\n[example: 1sad46575433sdas23423]: ")
    REDIRECT_URI = raw_input("\nEnter your Call Back or Redirect URL and port\n[example: http://127.0.0.1:8080]: ")

    # Write changes to appconfig.conf
    make_change = user_yes_no_query('\nAre you sure you want to write these changes?')
    if make_change == True:
        inplace_change('default/appconfig.conf', 'API_SERVER =', "API_SERVER = %s" % API_SERVER)
        inplace_change('default/appconfig.conf', 'WWW_SERVER =', "WWW_SERVER = %s" % WWW_SERVER)
        inplace_change('default/appconfig.conf', 'AUTHORIZE_URL =', "AUTHORIZE_URL = %s" % AUTHORIZE_URL)
        inplace_change('default/appconfig.conf', 'TOKEN_URL =', "TOKEN_URL = %s" % TOKEN_URL)
        inplace_change('default/appconfig.conf', 'SCOPES =', "SCOPES = %s" % SCOPES)
        inplace_change('default/appconfig.conf', 'SAMPLE_CALL =', "SAMPLE_CALL = %s" % SAMPLE_CALL)
        inplace_change('default/appconfig.conf', 'C_KEY =', "C_KEY = %s" % C_KEY)
        inplace_change('default/appconfig.conf', 'C_SECRET =', "C_SECRET = %s" % C_SECRET)
        inplace_change('default/appconfig.conf', 'REDIRECT_URI =', "REDIRECT_URI = %s" % REDIRECT_URI)

        print '\nAll Complete!'

    else:
        print '\nAll Complete!'

else:
    print '\nAll Complete!'

run_generator = user_yes_no_query('\nDo you want to run the generator now?')

# Run access_generator to get keys
if run_generator == True:
    system('python bin/access_generator.py')
else:
    print 'All done! Goodbye!'
    sys.exit()
