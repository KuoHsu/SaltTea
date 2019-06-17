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
    path('index/login/action/', views.login_action),
    path('index/logout/', views.logout),

    # 上傳資料
    path('index/upload/', views.upload_report),
    path('index/upload/action/', views.upload_action),

    # 呈現資料
    path('index/goTable/', views.go_table),
    path('index/boTable/', views.bo_table),
    path('index/gsTable/', views.gs_table),
    path('index/bsTable/', views.bs_table),
    path('index/goTable/action/', views.go_table_action),
    path('index/boTable/action/', views.bo_table_action),
    path('index/gsTable/action/', views.gs_table_action),
    path('index/bsTable/action/', views.bs_table_action),


    path('index/dataAnalysis/', views.data_analysis),
    path('index/dataAnalysis/query/', views.data_analysis_query),
    path('index/dataAnalysis/report/', views.data_analysis_report),
    path('index/analysisReport/', views.analysis_report),

] + staticfiles_urlpatterns('statics/')
