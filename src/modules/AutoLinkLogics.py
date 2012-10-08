#!/usr/bin/env python
''' SvxLinkWrapper - wrapper for SvxLink
Module to auto-connect Two logics together

Created on Oct 8, 2012
@author: Guy Sheffer <guysoft at gmail dot com>
'''
import SvxlinkwrapperModule
import time
import json

QSO_CALLSIGN_SEPERATOR=":"

class AutoLinkLogics(SvxlinkwrapperModule.SvxlinkwrapperModule):
    ''' Module to handle autoconnect to stations at startup '''
    def __init__(self,SvxLink):
        #Init
        SvxlinkwrapperModule.SvxlinkwrapperModule.__init__(self, SvxLink)
        self.CONNECT_COMMAND=self.getConfigVar("CONNECT_COMMAND")
        self.SECOND_LOGIC=self.getConfigVar("SECOND_LOGIC")
        return
    
    def handleStdout(self,line):
        '''
        Every stdout message would call this function
        '''
        
        if line.startswith("Starting logic: " + self.SECOND_LOGIC):
            self.SvxLink.sendToSvxLink(self.CONNECT_COMMAND)#Open echolink
        
        return
