"""sa_final URL Configuration

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
from fa_system import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [

    path('admin/', admin.site.urls),

    # 首頁
    path('', views.index),
    path('index/', views.index),
    path('accounts/login/', views.index),

    # 簡單頁面
    path('index/product/', views.product),
    path('index/about/', views.about),

    # 登入/登出
    path('index/login/', views.login),
    path('index/login/action/', views.loginAction),
    path('index/logout/', views.fun),

    # 上傳資料
    path('index/upload/', views.uploadReport),
    path('index/upload/action/', views.uploadAction),

    # 呈現資料
    path('index/goTable/', views.goTable),
    path('index/boTable/', views.boTable),
    path('index/gsTable/', views.gsTable),
    path('index/bsTable/', views.bsTable),
    path('index/goTable/action/', views.goTableAction),
    path('index/boTable/action/', views.boTableAction),
    path('index/gsTable/action/', views.gsTableAction),
    path('index/bsTable/action/', views.bsTableAction),


    path('index/dataAnalysis/', views.dataAnalysis),
    path('index/dataAnalysis/query/', views.dataAnalysisQuery),
    path('index/dataAnalysis/report/', views.dataAnalysisReport),
    path('index/analysisReport/', views.analysisReport),

] + staticfiles_urlpatterns('statics/')
