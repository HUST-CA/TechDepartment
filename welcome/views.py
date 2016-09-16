from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.core.mail import send_mail
from django.template import Context, Template

from . import forms
from .models import NewMember

import top.api


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
            return render(request, self.template_name, {'form': form})
        else:
            messages.add_message(request, messages.WARNING, '报名失败，请查看各项后的错误提示。')
            return render(request, self.template_name, {'form': form})
