# _*_ encoding:utf-8 _*_
# author:ElegyPrincess
from django import forms
from captcha.fields import CaptchaField


class DataForm(forms.Form):
    captcha=CaptchaField()