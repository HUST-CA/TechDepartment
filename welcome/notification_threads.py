#coding=utf-8
from django.core.mail import send_mass_mail
from django.conf import settings
from welcome import calc_sign
from welcome import send_sms

import threading
import json
import time

'''
Takes a tuple of messages and send them

A message is a tuple containing these four elements:
(subject, message, from_email, recipient_list)
'''
class MassEmailSenderThread(threading.Thread):
    def __init__(self, messages, daemon):
        '''
        messages[0] -> first message
                   [3] -> recipient_list in first message
                      [0] -> first address in recipient_list
        '''
        firstReceiverName = messages[0][3][0].split("@", 1)[0]
        super(MassEmailSenderThread, self).__init__(name = "EmailSenderThread-" + firstReceiverName, daemon=daemon)
        self.messages = messages
        
    def run(self):
        send_mass_mail(self.messages)

'''
Takes REST service API URL and SMS params to send a short message

For AliDayu. Read its documentation for the params.
The "sign" parameter will be calculated here. No need to add in the params.
'''
class SMSSenderThread(threading.Thread):
    def __init__(self, url, params, daemon):
        firstReceiverName = json.loads(params['sms_param'])['name']
        super(SMSSenderThread, self).__init__(name = "SMSSenderThread-" + firstReceiverName, daemon=daemon)
        self.url = url
        self.params = params
        
    def run(self):
        sign = calc_sign.calc_sign(self.params, settings.SECRET)
        self.params['sign'] = sign
        send_sms.send_sms(self.url, self.params)

