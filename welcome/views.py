from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.core.mail import send_mail
from django.template import Context, Template

from . import forms
from .models import NewMember
from django.conf import settings

import urllib.request, urllib.parse
from urllib.error import URLError, HTTPError
import time
import datetime


class IndexView(generic.View):
    pass


class WelcomeView(generic.View):
    template_name = 'welcome/welcome.html'

    def get(self, request):
        form = forms.WelcomeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.WelcomeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            NewMember.objects.create(**cd)
            messages.add_message(request, messages.SUCCESS, '报名成功,请确认收到短信或邮件！')
            send_mail(
                subject='计算机协会技术部报名',
                message='【计算机协会技术部】亲爱的' + cd['name'] + '同学，你好：\n        我们已经收到了你的报名信息，请耐心等待后续通知消息，谢谢。',
                from_email='HUSTCA <info@hustca.com>',
                recipient_list=[cd['email']],
            )
            messages_template = Template('''【技术部招新】有成员填写表单，请注意查看后台。
                        姓名:{{ name }}
                        性别:{{ sex }}（1为男0为女）
                        电话:{{ tel }}
                        邮箱:{{ email }}
                        专业-年级:{{ college }}
                        寝室住址:{{ dormitory }}
                        小组意向:{{ group }}
                        自我介绍:{{ introduction }}
                ''')
            context = Context(cd)
            send_mail(
                subject='计算机协会技术部报名',
                message=messages_template.render(context),
                from_email='HUSTCA <info@hustca.com>',
                recipient_list=['engineering@hustca.com'],
            )

            # url = 'http://gw.api.taobao.com/router/rest'
            # values = {
            #     'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            #     'app_key': settings.APPKEY,
            #     'format': 'json',
            #     'method': 'alibaba.aliqin.fc.sms.num.send',
            #     'partner_id': 'apidoc',
            #     'sign': settings.SECRET,
            #     'sign_method': 'hmac',
            #     'timestamp': datetime.datetime.utcfromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"),
            #     'v': '2.0',
            #     'extend': cd['name'],
            #     'rec_num': '13007100014',
            #     'sms_free_sign_name': '计算机协会技术部',
            #     'sms_param': cd['name'],
            #     'sms_template_code': settings.SMS_TEMPLATE_CODE,
            #     'sms_type': 'normal',
            # }
            # url_values = urllib.parse.urlencode(values).encode(encoding='UTF8')
            # full_url = urllib.request.Request(url, url_values)
            # try:
            #     response = urllib.request.urlopen(full_url)
            # except HTTPError as e:
            #     print('Error code:', e.code)
            # except URLError as e:
            #     print('Reason', e.reason)
            # the_page = response.read()
            # print(the_page)

            return render(request, self.template_name, {'form': form})
        else:
            messages.add_message(request, messages.WARNING, '报名失败，请查看各项后的错误提示。')
            return render(request, self.template_name, {'form': form})
