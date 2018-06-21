from django.http import HttpResponse
from django.shortcuts import render
import requests
from django.views import View
from RecognizeCaptcha.settings import BASE_DIR
from apps.ProduceData.forms import DataForm
import os
import MySQLdb

Train_image_files = os.path.join(BASE_DIR, 'media', 'train')
Test_image_files=os.path.join(BASE_DIR, 'TestFile')

class GetDataView(View):
    def get(self,request):
        data_form=DataForm()
        return render(request,"GetData.html",{'data_form':data_form})

    def post(self,request):
        if not os.path.exists(Train_image_files):
            os.mkdir(Train_image_files)
        url=request.POST.get("src","")
        hashkey=request.POST.get("hashkey","")
        db = MySQLdb.connect(host="localhost", user="root", passwd="888212", db="recognizecaptcha")
        c = db.cursor()
        c.execute("SELECT * FROM captcha_captchastore where hashkey = '"+hashkey+"';")
        result = c.fetchone()

        r = requests.get(url, stream=True)
        with open(os.path.join(Train_image_files,result[1]+'.png'), 'wb') as fd:
            for chunk in r.iter_content():
                fd.write(chunk)

        return HttpResponse('{"msg":"success"}', content_type='application/json')


class GetTestDataView(View):
    def post(self,request):
        if not os.path.exists(Test_image_files):
            os.mkdir(Test_image_files)
        url=request.POST.get("src","")
        hashkey=request.POST.get("hashkey","")

        db = MySQLdb.connect(host="localhost", user="root", passwd="888212", db="recognizecaptcha")
        c = db.cursor()
        c.execute("SELECT * FROM captcha_captchastore where hashkey = '"+hashkey+"';")
        result = c.fetchone()

        r = requests.get(url, stream=True)
        with open(os.path.join(Test_image_files,result[1]+'.png'), 'wb') as fd:
            for chunk in r.iter_content():
                fd.write(chunk)

        return HttpResponse('{"msg":"success"}', content_type='application/json')