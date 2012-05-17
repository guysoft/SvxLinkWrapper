#!/usr/bin/env python
''' SvxLinkWrapper - wrapper for SvxLink
Module that logs all qsos in a sqlite database

Created on Feb 1, 2012
@author: Guy Sheffer <guysoft at gmail dot com>
'''
import sqlite3
import time
import re

from SvxlinkwrapperModule import SvxlinkwrapperModule

QSO_CALLSIGN_SEPERATOR=":"
class dataControl:
    '''
    This is a class that connects to the sqlite3 database
    You could in theory re-implement it to use any other kind of database
    '''
    def __init__(self,moduleConfigDict):
        #Init QSO Database
        self.DATABASE_PATH=moduleConfigDict["database_path"]
        self.conn = sqlite3.connect(self.DATABASE_PATH)
        return
        
    def insertQSO(self,ips,names,cs,state):
        try:   
            c = self.conn.cursor()
            
            ip=""
            name=""
            if ips.has_key(cs):
                ip =ips[cs]
            if names.has_key(cs):
                name =names[cs]
            
            # Insert a row of data
            sql = "insert into qso values (?,?,?,?,?,?)"
            variables = (cs,None,ip,buffer(name),state,str(time.time()))
            
            c.execute(sql,variables)    
            # Save (commit) the changes
            self.conn.commit()
        finally:
            c.close()
        return
    
    def startQSO(self,cs,names,ips):
        #print (cs)
        #print(names)
        #print(ips)
        self.insertQSO(ips,names,cs,"enter")
        return
    
    def endQSO(self,cs,names,ips):
        self.insertQSO(ips,names,cs,"exit")
        return

class EcholinkLoggerModule(SvxlinkwrapperModule):
    def __init__(self,SvxLink):
        SvxlinkwrapperModule.__init__(self,SvxLink)
        
        #Dict of cs and the name from echolink
        self.csName={}
        self.csIP={}
        moduleConfigDict=self.getConfigFullDict()
        self.database = dataControl(moduleConfigDict)
        return
    
    def handleStdout(self,line):
        '''
        Every stdout message would call this function
        '''
        
        if line.endswith("EchoLink QSO state changed to CONNECTED\n"):
            station = line.split(QSO_CALLSIGN_SEPERATOR)[0]
            self.database.startQSO(station,self.csName,self.csIP)
            
        if line.endswith("EchoLink QSO state changed to DISCONNECTED\n"):
            station = line.split(QSO_CALLSIGN_SEPERATOR)[0]
            self.database.endQSO(station,self.csName,self.csIP)
        
        if line.startswith("Incoming EchoLink connection from"):
                #Incoming EchoLink connection from 4Z7GAI (Guy) at 127.0.0.1
                m = re.compile('Incoming EchoLink connection from (.*) \((.*)\) at (.*)\n').match(line)
                cs = m.group(1)
                name = m.group(2)
                ip= m.group(3)
                self.csName[cs]=name
                self.csIP[cs]=ip
                return
        return
