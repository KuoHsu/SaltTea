"""systemAna URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from front.views import *
from systemAna import settings
#from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('index', index),
    path('index/login', login),
    path('index/logout', logout),
    path('index/login/action', loginAction),
    path('index/uploadReport', uploadReport),
    path('index/uploadReport/action', uploadReportAction),
    path('index/goTable', goTable),
    path('index/boTable', boTable),
    path('index/gsTable', gsTable),
    path('index/bsTable', bsTable),
    path('index/dataAnalysis', dataAnalysis),
    path('index/analysisReport', analysisReport),
    path('index/about', about),
] + staticfiles_urlpatterns('statics/')
