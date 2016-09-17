from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template import Context, Template
from django.conf import settings

from . import models
from . import calc_sign
from . import send_sms

import time
import datetime


@receiver(post_save, sender=models.NewMember)
def create_profile_handler(sender, instance, created, **kwargs):
    if not created:
        return
        # send the message only if new member is coming
    send_mail(
        subject='计算机协会技术部报名',
        message='【计算机协会技术部】亲爱的' + instance.name + '同学，你好：\n        我们已经收到了你的报名信息，请耐心等待后续通知消息，谢谢。',
        from_email='HUSTCA <info@hustca.com>',
        recipient_list=[instance.email],
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
    send_mail(
        subject='计算机协会技术部报名',
        message=messages_template.render(context),
        from_email='HUSTCA <info@hustca.com>',
        recipient_list=['engineering@hustca.com'],
    )

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
        'timestamp': str(int(time.mktime(datetime.datetime.now().timetuple()))),
        'v': '2.0',
    }
    sign = calc_sign.calc_sign(values, settings.SECRET)
    values['sign'] = sign
    send_sms.send_sms(url, values)