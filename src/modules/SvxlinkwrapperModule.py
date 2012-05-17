#!/usr/bin/env python
''' SvxLinkWrapper - wrapper for SvxLink
This is a template module that all other svxlinkwrapper modules extend

Created on Feb 1, 2012
@author: Guy Sheffer <guysoft at gmail dot com>
'''
import json

def turpleList2Dict(tupleList):
    ''' Convert a tuple list to a dict. For easy and saner access
    Used in this project because config parser returns a list of tuples
    @param tupleList the list of tuples
    @return: a dict with lists for each variable
    '''
    returnDict={}
    for turple in tupleList:
        key = turple[0]
        data = turple[1]
        if data.startswith("["):#turn to a list if lists
            data = json.loads(data)
        returnDict[key]=data
    return returnDict

class SvxlinkwrapperModule(object):
    def __init__(self,SvxLink):
        self.SvxLink = SvxLink
        return
    
    def handleStdout(self,line):
        '''
        Every stdout message would call this function
        '''
        return
    
    def shutdown(self):
        '''
        Runs when we get ctrl-c to exit
        '''
        return
    
    def getConfigVar(self,value):
        '''Get a value from the config ini for a module
        @param value - the value you wnat
        @return: the value from config.ini 
        '''
        return self.SvxLink.config.get("modules."+self.__class__.__name__, value)
    
    def getConfigList(self,value):
        '''Get a value from the config ini for a module
        @param value - the value you wnat
        @return: the value from config.ini 
        '''
        return json.loads(self.SvxLink.config.get("modules."+self.__class__.__name__, value))
    
    def getConfigFullDict(self):
        ''' Get the whole config as a dict, useful if you need to move it to other clases
        @return: a dict with all the config vars from config.ini
        '''
        return turpleList2Dict(self.SvxLink.config.items("modules."+self.__class__.__name__))
