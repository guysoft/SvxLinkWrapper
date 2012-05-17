#!/usr/bin/env python
''' SvxLinkWrapper - wrapper for SvxLink
Main

Created on Dec 6, 2011
@author: Guy Sheffer <guysoft at gmail dot com>
'''

import json

import sys
import os.path
import modules.SvxlinkwrapperModule
from subprocess import PIPE, Popen
from straight.plugin import load

from ConfigParser import SafeConfigParser

def appendProjectPath(path='.'):
    ''' Appends the project path to a relative path
    @param path: the internal path
    @return: the relative path 
    '''
    return os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),path)


def loadConfig():
    ''' Get the config file and folder
    @return: a turple with a config parser to config.ini and the etc folder'''
    config = SafeConfigParser()
    ETC_DIR= appendProjectPath()
    config.read(os.path.join(ETC_DIR,"config.ini"))
    return config,ETC_DIR
config,ETC_DIR = loadConfig()


SVXLINK_CMD = config.get('main', 'SVXLINK_CMD')
dirname, filename = os.path.split(os.path.abspath(__file__))
MODULES_DIR=config.get('main', 'MODULES_DIR')
PLAY_SOUND_COMMAND = os.path.join(dirname,config.get('main', 'PLAY_SOUND_COMMAND'))
TONES_PATH = os.path.join(dirname,'..',config.get('main', 'TONES_PATH'))
SOUNDS_PATH = os.path.join(dirname,'..',config.get('main', 'SOUNDS_PATH'))

pluginLoadList=json.loads(config.get("main","pluginLoadList"))

plugins = load(MODULES_DIR,subclasses=modules.SvxlinkwrapperModule.SvxlinkwrapperModule)

class SvxLinkWrapper:
    '''
    Main SvxLinkWrapper
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.config = config
        #loads all the plugins listed in to self.plugins
        self.plugins = []
        for plugin in plugins:
            if plugin.__name__ in pluginLoadList:
                self.plugins.append(plugin(self))
                
        try:
            self.p = Popen(SVXLINK_CMD, stdout=PIPE, stderr=PIPE,stdin=PIPE)
            for line in iter(self.p.stdout.readline, ''):
                self.handleStdout(line)
        
        except KeyboardInterrupt:
            self.debug("Got Key interrupt")
            for plugin in self.plugins:
                plugin.shutdown()
            sys.exit(0)
            
        return
    
    def shutdown(self):
        os.system("kill " + os.getpid())
        return

    def handleStdout(self,line):
        '''
        Handle messages SVXLink outputs to the screen
        '''
        print (line[:-1])
        
        #iterate over all plugins and run handleStdout 
        for plugin in self.plugins:
            plugin.handleStdout(line)
        return
    
    def playsound(self,sound):
                
        command = PLAY_SOUND_COMMAND + " " + SOUNDS_PATH + sound
        print (command)
        os.system(command)
        return
    
    def debug(self,message):
        print ("SVXLinkWrapper:" + message)
        return
        
    def dtmfSTR(self,string):
        string = string.replace("*", "s")
        string = string.replace("#", "p")
        returnValue = ""
        for tone in string:
            returnValue+= " '" + os.path.join(TONES_PATH,tone + ".wav") + "' "
        return returnValue
    
    def sendToSvxLink(self,message):
        self.p.stdin.write(message)
        return

if __name__ == '__main__':
    a = SvxLinkWrapper()
    sys.exit(0)