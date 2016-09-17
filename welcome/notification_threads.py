#coding=utf-8
from django.core.mail import send_mail
from django.conf import settings
from welcome import calc_sign
from welcome import send_sms

import threading
import json
import time

class EmailSenderThread(threading.Thread):
    def __init__(self, subject, message, from_email, recipient_list):
        firstReceiverName = recipient_list[0].split("@", 1)[0]
        super(EmailSenderThread, self).__init__(name = "EmailSenderThread-" + firstReceiverName)
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.recipient_list = recipient_list
        
    def run(self):
        send_mail(self.subject, self.message, self.from_email, self.recipient_list)

class SMSSenderThread(threading.Thread):
    def __init__(self, url, params):
        firstReceiverName = json.loads(params['sms_param'])['name']
        super(SMSSenderThread, self).__init__(name = "SMSSenderThread-" + firstReceiverName)
        self.url = url
        self.params = params
        
    def run(self):
        sign = calc_sign.calc_sign(self.params, settings.SECRET)
        self.params['sign'] = sign
        send_sms.send_sms(self.url, self.params)

