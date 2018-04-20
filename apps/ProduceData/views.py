from django.http import HttpResponse
from django.shortcuts import render
import requests
from django.views import View

from apps.ProduceData.forms import DataForm

import MySQLdb

class GetDataView(View):
    def get(self,request):
        data_form=DataForm()
        return render(request,"GetData.html",{'data_form':data_form})

    def post(self,request):
        url=request.POST.get("src","")
        hashkey=request.POST.get("hashkey","")

        db = MySQLdb.connect(host="localhost", user="root", passwd="888212", db="recognizecaptcha")
        c = db.cursor()
        c.execute("SELECT * FROM captcha_captchastore where hashkey = '"+hashkey+"';")
        result = c.fetchone()

        r = requests.get(url, stream=True)
        with open('./media/train/'+result[1]+'.png', 'wb') as fd:
            for chunk in r.iter_content():
                fd.write(chunk)

        return HttpResponse('{"msg":"success"}', content_type='application/json')

