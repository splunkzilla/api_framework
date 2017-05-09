import splunk.admin as admin
import splunk.entity as en
# import your required python modules

'''
Copyright (C) 2005 - 2010 Splunk Inc. All Rights Reserved.
Description:  This skeleton python script handles the parameters in the configuration page.
      handleList method: lists configurable parameters in the configuration page
      corresponds to handleractions = list in restmap.conf
      handleEdit method: controls the parameters and saves the values
      corresponds to handleractions = edit in restmap.conf
'''

class ConfigApp(admin.MConfigHandler):
  '''
  Set up supported arguments
  '''
  def setup(self):
    if self.requestedAction == admin.ACTION_EDIT:
      for arg in ['C_KEY', 'C_SECRET', 'REDIRECT_URI', 'DATE_INTERVAL', 'TIME_INTERVAL', 'TIME_DELAY']:
        self.supportedArgs.addOptArg(arg)

  '''
  Read the initial values of the parameters from the custom file
      myappsetup.conf, and write them to the setup screen.
  If the app has never been set up,
      uses .../<APPNAME>/default/myappsetup.conf.
  If app has been set up, looks at
      .../local/myappsetup.conf first, then looks at
  .../default/myappsetup.conf only if there is no value for a field in
      .../local/myappsetup.conf
  For boolean fields, may need to switch the true/false setting.
  For text fields, if the conf file says None, set to the empty string.
  '''

  def handleList(self, confInfo):
    confDict = self.readConf("appconfig")
    if None != confDict:
      for stanza, settings in confDict.items():
        for key, val in settings.items():
          if key in ['C_KEY'] and val in [None, '']:
            val = ''
          if key in ['C_SECRET'] and val in [None, '']:
            val = ''
          confInfo[stanza].append(key, val)

  '''
  After user clicks Save on setup screen, take updated parameters,
  normalize them, and save them somewhere
  '''
  def handleEdit(self, confInfo):
    name = self.callerArgs.id
    args = self.callerArgs
    if self.callerArgs.data['C_KEY'][0] in [None, '']:
      self.callerArgs.data['C_KEY'][0] = 'ABC123'

    if self.callerArgs.data['C_SECRET'][0] in [None, '']:
      self.callerArgs.data['C_SECRET'][0] = '1234567890abcefgh1234567890abcdef'

    if self.callerArgs.data['REDIRECT_URI'][0] in [None, '']:
      self.callerArgs.data['REDIRECT_URI'][0] = 'http://127.0.0.1:8080'


    '''
    Since we are using a conf file to store parameters,
write them to the [setupentity] stanza
    in <APPNAME>/local/myappsetup.conf
    '''

    self.writeConf('appconfig', 'Authentication', self.callerArgs.data)
    self.writeConf('appconfig', 'Activity', self.callerArgs.data)

# initialize the handler
admin.init(ConfigApp, admin.CONTEXT_NONE)