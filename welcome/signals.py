from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import Context, Template
from django.conf import settings

from welcome.notification_threads import MassEmailSenderThread
from welcome.notification_threads import SMSSenderThread

from . import models

import time


@receiver(post_save, sender=models.NewMember)
def inform(sender, instance, created, **kwargs):
    if not created:
        return
        # send the message only if new member is coming
    greet_email_tuple = (
        '计算机协会技术部报名',
        '【计算机协会技术部】亲爱的' + instance.name + '同学，你好：\n        我们已经收到了你的报名信息，请耐心等待后续通知消息，谢谢。请记得加入招新QQ群0810，也可点击此链接直接加入： http://excited.haha.im/?xu=1s',
        'HUSTCA <info@hustca.com>',
        [instance.email],
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
    context = Context(
        {
            'name': instance.name,
            'sex': instance.sex,
            'tel': instance.tel,
            'email': instance.email,
            'college': instance.college,
            'dormitory': instance.dormitory,
            'group': instance.group,
            'introduction': instance.introduction,
        }
    )
    internal_email_tuple = (
        '计算机协会技术部报名',
        messages_template.render(context),
        'HUSTCA <info@hustca.com>',
        ['engineering@hustca.com'],
    )
    mass_mail_sender_thread = MassEmailSenderThread(messages=(greet_email_tuple, internal_email_tuple))
    mass_mail_sender_thread.start()

    url = 'http://gw.api.taobao.com/router/rest'
    values = {
        'app_key': settings.APPKEY,
        'format': 'json',
        'method': 'alibaba.aliqin.fc.sms.num.send',
        'partner_id': 'apidoc',
        'rec_num': instance.tel,
        'sign_method': 'md5',
        'sms_free_sign_name': 'HUST计协',
        'sms_param': '{"name":"' + instance.name + '"}',
        'sms_template_code': settings.SMS_TEMPLATE_CODE,
        'sms_type': 'normal',
        # 'timestamp': datetime.datetime.utcfromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"),
        # please use a unix timestamp
        'timestamp': str(int(time.time())),
        'v': '2.0',
    }
    sms_sender_thread = SMSSenderThread(url, values)
    sms_sender_thread.start()

