#!/usr/bin/env python
''' SvxLinkWrapper - wrapper for SvxLink
Module to handle echolink incoming chat message and parse them

Created on Feb 1, 2012
@author: Guy Sheffer <guysoft at gmail dot com>
'''
import SvxlinkwrapperModule

'''
Module to handle echolink incoming chat message and parse them
'''
class EcholinkChatModule(SvxlinkwrapperModule.SvxlinkwrapperModule):
    '''
    plugin to handle incoming chat message and parse them
    '''
    def __init__(self,SvxLink):
        SvxlinkwrapperModule.SvxlinkwrapperModule.__init__(self, SvxLink)
        self.inChatMessage=False
        self.chatUser = ""
        return
    
    def handleStdout(self,line):
        '''
        Every stdout message would call this function
        '''
        '''
        eg chat message:
        --- EchoLink chat message received from 4Z7GAI ---
        4Z7GAI>test
        '''
        
        #Handle if we are already in a chat message
        if self.inChatMessage:
            self.SvxLink.debug(line)
            try:
                data = line.split(">")
                data[1] = (data[1])[:-1]
                self.handleChatMessage(data)
            except:
                pass
            self.inChatMessage = False
        
        #Handle if we are not in a chat message
        if line.startswith("--- EchoLink chat message received from"):
            self.inChatMessage = True
            self.chatUser = line.split("from ")[1]   
        return
    
    def handleChatMessage(self,data):
        '''
        This function runs every time we get an echolink chat message
        Note you can check who sent the mesasge with self.chatUser
        '''
        return
    