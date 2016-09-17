from django.shortcuts import render
from django.views import generic
from django.contrib import messages
# from django.core.mail import send_mail
# from django.template import Context, Template
# from django.conf import settings

from . import forms
from .models import NewMember
# from . import calc_sign
# from . import send_sms

# import time
# import datetime


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
            del cd['captcha']
            NewMember.objects.create(**cd)
            messages.add_message(request, messages.SUCCESS, '报名成功,请确认收到短信或邮件！')
            return render(request, self.template_name, {'form': form})
        else:
            messages.add_message(request, messages.WARNING, '报名失败，请查看各项后的错误提示。')
            return render(request, self.template_name, {'form': form})

