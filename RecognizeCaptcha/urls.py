"""RecognizeCaptcha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.static import serve

from apps.ProduceData.views import GetDataView
from RecognizeCaptcha.settings import STATICFILES_DIRS,MEDIA_ROOT

urlpatterns = [
    url(r'^getData/$',GetDataView.as_view(),name="getData"),
    url(r'^static/(?P<path>.*)$',serve,{"document_root":STATICFILES_DIRS}),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', admin.site.urls),
]
