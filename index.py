#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fbchat import log, Client
from fbchat.models import *
import os
import re
from random import randint
import getpass
password =  getpass.getpass(prompt='Password: ', stream=None)
mail = getpass.getpass(prompt='Mail: ', stream=None)
questpermission = True
ranswer = None
rcomment = None
random = 0
i = 0
questionarr = []
direct = 'answers/'
for root, dirs, filenames in os.walk(direct):
    for fname in filenames:
        i+=1
        file = open("answers/%s" % fname, "r")
        answer =  file.read()
        question = fname.replace('.txt','')
        file.close()
        file = open("comment/%s" % fname, "r")
        comment =  file.read()
        file.close()
        questionarr.append([question,answer,comment])



class EchoBot(Client):
    def onListening(self):
            global ranswer
            global questpermission
            global i
            global random
            global rcomment
            random = randint(0, i-1)
            questelement = questionarr[random]
            ranswer=questelement[1].decode('utf-8').upper().encode('utf-8')
            rcomment=questelement[2]
            self.sendLocalImage("questions/%s"%questelement[0], message=None, thread_id="1286566608131059", thread_type=ThreadType.GROUP)
            questpermission = False
    def onMessageSeen(self, seen_by=None, thread_id="1286566608131059", thread_type=ThreadType.GROUP, seen_ts=None, ts=None, metadata=None, msg=None):
        global ranswer
        global questpermission
        global i
        global random
        global rcomment
        if questpermission:
            random = randint(0, i-1)
            questelement = questionarr[random]
            ranswer=questelement[1].decode('utf-8').upper().encode('utf-8')
            rcomment=questelement[2]
            self.sendLocalImage("questions/%s"%questelement[0], message=None, thread_id="1286566608131059", thread_type=ThreadType.GROUP)
            questpermission = False
    def onMessage(self, author_id,message, message_object, thread_id, thread_type, **kwargs):
        global ranswer
        global questpermission
        global i
        global random
        global rcomment
        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)
        if author_id != self.uid:
            if i==0:
                self.send(Message(text='No question left'), thread_id=thread_id, thread_type=thread_type)
                self.listening = False
            mtext = message_object.text.upper().encode('utf-8')
            message_object.attachments=ImageAttachment
            if   questpermission==False:
                if mtext == ranswer or mtext=="WASTED!":
                    self.send(Message(text='Ответ:%s' % ranswer), thread_id=thread_id, thread_type=thread_type)
                    self.send(Message(text='Комментарий:%s' % rcomment), thread_id=thread_id, thread_type=thread_type)
                    del questionarr[random]
                    i-=1
                    questpermission=True
                    ranswer = None

client = EchoBot(mail, password)
client.listen()
