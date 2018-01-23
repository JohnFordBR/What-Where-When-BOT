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
    def onMessage(self, author_id,message, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)
        global ranswer
        global questpermission
        global i
        global random
        global rcomment
        if author_id != self.uid:
            if i==0:
                self.send(Message(text='No question left'), thread_id=thread_id, thread_type=thread_type)
                self.listening = False
            mtext = message_object.text.encode('utf-8')
            message_object.attachments=ImageAttachment
            # print(mtext.decode('utf-8').upper().encode('utf-8'))
            if   questpermission==False:
                if mtext.decode('utf-8').upper().encode('utf-8') == ranswer.upper() or mtext=="Wasted!":
                    self.send(Message(text='Ответ:%s' % ranswer), thread_id=thread_id, thread_type=thread_type)
                    self.send(Message(text='Комментарий:%s' % rcomment), thread_id=thread_id, thread_type=thread_type)
                    del questionarr[random]
                    i-=1
                    questpermission=True
                    ranswer = None
            elif mtext == "Give question!" and questpermission:
                random = randint(0, i-1)
                questelement = questionarr[random]
                ranswer=questelement[1]
                rcomment=questelement[2]
                self.sendLocalImage("questions/%s"%questelement[0], message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
                questpermission = False

client = EchoBot(mail, password)
client.listen()
