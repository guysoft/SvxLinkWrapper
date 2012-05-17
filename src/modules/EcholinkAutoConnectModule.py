#!/usr/bin/env python
''' SvxLinkWrapper - wrapper for SvxLink
Module to auto-connect to stations on startup

Created on Feb 1, 2012
@author: Guy Sheffer <guysoft at gmail dot com>
'''
import SvxlinkwrapperModule
import time
import json

QSO_CALLSIGN_SEPERATOR=":"

class EcholinkAutoConnectModule(SvxlinkwrapperModule.SvxlinkwrapperModule):
    ''' Module to handle autoconnect to stations at startup '''
    def __init__(self,SvxLink):
        #Init
        SvxlinkwrapperModule.SvxlinkwrapperModule.__init__(self, SvxLink)
        #Values
        self.STATIONS=json.loads(self.getConfigVar("STATIONS"))
        self.MAX_ATTEMPTS=int(self.getConfigVar("MAX_ATTEMPTS"))
        self.ECHOLINK_OPEN=self.getConfigVar("ECHOLINK_OPEN")
        self.connection_attempts={}
        
        
        for station in self.STATIONS:
            self.connection_attempts[station]=0;
        return
    
    def connectToStation(self,station):
        if (self.connection_attempts[station] < self.MAX_ATTEMPTS) or (self.MAX_ATTEMPTS == 0):
            self.SvxLink.sendToSvxLink(self.STATIONS[station]+'#')#Open station
            self.connection_attempts[station] = self.connection_attempts[station] + 1
        return
    
    def handleStdout(self,line):
        '''
        Every stdout message would call this function
        '''
        
        if line.startswith("--- EchoLink directory server message: ---"):
            self.SvxLink.sendToSvxLink(self.ECHOLINK_OPEN)#Open echolink
            for station in self.STATIONS:
                self.connectToStation(station)
        
        
        if line.endswith("EchoLink QSO state changed to DISCONNECTED\n"):
            station = line.split(QSO_CALLSIGN_SEPERATOR)[0]
            
            self.SvxLink.debug(station)
            if station in self.STATIONS:
                self.SvxLink.debug("Reconnecting to " + station)
                time.sleep(8)
                self.connectToStation(station)
        return
