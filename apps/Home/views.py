from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import json
from RecognizeCaptcha.settings import BASE_DIR
from apps.ProduceData.forms import DataForm
from apps.RecognizeData.SolveCaptcha import RecognizeCaptcha
from apps.Home.models import picModel
import os

Test_image_files=os.path.join(BASE_DIR, 'TestFile')

class HomeView(View):
    def get(self,request):
        if not os.path.exists(Test_image_files):
            os.mkdir(Test_image_files)
        data_form = DataForm()
        return render(request,"index.html",{'data_form':data_form})

class RecognizeView(View):
    def post(self,request):
        picFile = request.FILES['picture']
        pic=picModel(pic=picFile)
        pic.save()
        captcha_text=RecognizeCaptcha(str(picFile))
        dict={
            "status":"true",
            "msg":captcha_text,
        }
        text=json.dumps(dict)
        return HttpResponse(text, content_type='application/json')
