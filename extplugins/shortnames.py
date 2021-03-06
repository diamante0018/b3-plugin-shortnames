__version__ = '1.0'
__author__ = 'Zwambro'

import b3
import b3.events
import b3.plugin
import string
import re

class ShortnamesPlugin(b3.plugin.Plugin):
    _adminPlugin = False
    requiresConfigFile = False

    def onStartup(self):

        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.debug('Could not find admin plugin')
            return False
        else:
            self.debug('Plugin loaded normal')
        self.registerEvent(b3.events.EVT_CLIENT_AUTH)
        self.debug('Started')

    def onEvent(self, event):
        """
        First we use regular expressions to remove to remove whitespaces, if the length is less than 3 we kick.
        Lastly we check for non printable characters, if we find them we ban the player.
        """
        if event.type == b3.events.EVT_CLIENT_AUTH:
            name = str(event.client.name)
            r = re.compile(r'\s+', re.UNICODE)
            name = re.sub(r, '', name)
            
            if len(name) < 3:
                self.debug("(%s) has short name" %(name))
                event.client.kick("Are you bot?", keyword="short_name")
                return True
            else:
                self.debug('Client has more than 3 characters in his IGN')
                
            if not (all(c in string.printable for c in name)):
                self.debug('(%s) has non printable characters in his name' %(name))
                event.client.ban("Are you bot?", keyword="short_name")
                return True
            else:
                self.debug('Client name is printable')

            return False
