# -*- coding: utf-8 -*-
#
# BadNick for UrbanTerror plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2015 PtitBigorneau - www.ptitbigorneau.fr
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '2'


import b3, time, threading, thread
import b3.events
import b3.plugin

from b3.functions import getCmd

class BadnickPlugin(b3.plugin.Plugin):

    _adminPlugin = None
    _protectlevel = 20
	
    def onLoadConfig(self):

        self._protectlevel = self.getSetting('settings', 'protectlevel', b3.LEVEL, self._protectlevel)

    def onStartup(self):

        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:

            self.error('Could not find admin plugin')
            return False
			
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = getCmd(self, cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

        self.registerEvent('EVT_CLIENT_AUTH', self.onClientEvt)
        self.registerEvent('EVT_CLIENT_NAME_CHANGE', self.onClientEvt)

    def onClientEvt(self, event):
            
        test = None
        sclient = event.client
        cnamemin = sclient.name.lower()
		
        for x in sclient.name:
            if str.isalpha(x) == True:
               test = "ok"
           
        if (sclient.name.isdigit()) or (len(sclient.name) < 2) or ('//' in cnamemin) or not test:
                
            name = sclient.name        
            thread.start_new_thread(self.cmdbadnick, (sclient, name, "pause"))

    def cmd_badnick(self, data, client, cmd=None):
        
        """\
        <name> - Player name with Bad Nickname
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            
            client.message('!badnick <player name>')
            return
        
        sclient = self._adminPlugin.findClientPrompt(input[0], client)
        
        if not sclient:
            
            return False
      
        if sclient.maxLevel >= self._protectlevel:
            
            client.message('^3Invalid Command on %s!' %(sclient.exactName))
            return False

        if sclient:        
            
            name = sclient.name        
            thread.start_new_thread(self.cmdbadnick, (sclient, name, None))
            
        else:
            return False
    
    def cmdbadnick(self, sclient, name, pause):
	
        if pause:
            time.sleep(15)

        reps = 3
            
        self.console.say('%s^1 Bad Nickmane !'%(sclient.exactName))
            
        while reps > 0:
                
            for cid,x in self.console.clients.items():

                if x == sclient:
                        
                    if name == sclient.name :
                                    
                        self.console.write('forceteam %s %s' %(sclient.cid, 's'))
                        self._adminPlugin.warnClient(sclient, '^3Bad NickName', None, False, '', 60)
                        sclient.message('^3Change your NickName !')       
                    else:
                        return False
            
            time.sleep(20)
            reps-=1

  
