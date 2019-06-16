from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

# Create your views here.


def getUserInfo(request):
    r = dict()
    r['login'] = request.session.get('login', False)
    r['username'] = request.session.get('username', '')
    r['permission'] = request.session.get('permission', 'guest')
    return r


def index(request):
    userInfo = getUserInfo(request)
    return render(request, 'index.html', userInfo)


def login(request):
    return render(request, 'login.html')


def logout(request):
    request.session['username'] = ''
    request.session['permission'] = 'guest'
    request.session['login'] = False
    return redirect('/index')


def loginAction(request):
    loginFlag = False
    if request.method == 'POST':
        acccount = request.POST.get('account', '')
        password = request.POST.get('password', '')

        if acccount in ['investor', 'branch', 'analysis', 'finDep']:
            request.session['username'] = acccount
            request.session['login'] = True
            loginFlag = True

        if acccount == 'investor' and password == '123':
            request.session['permission'] = 'investor'
        elif acccount == 'branch' and password == '123':
            request.session['permission'] = 'branch'
        elif acccount == 'analysis' and password == '123':
            request.session['permission'] = 'analysis'
        elif acccount == 'finDep' and password == '123':
            request.session['permission'] = 'finDep'

    response = HttpResponse()
    response.content = json.dumps({'loginFlag': loginFlag})
    return response


def uploadReport(request):
    userInfo = getUserInfo(request)
    return render(request, 'uploadReport.html', userInfo)


def uploadReportAction(request):
    response = HttpResponse()
    data = dict()
    if request.method == 'POST':
        data['file'] = request.POST.get('file', None)
        data['category'] = request.POST.get('reportC', '')
        data['uploadFlag'] = True
    response.content = json.dumps(data)
    return response


def goTable(request):
    userInfo = getUserInfo(request)
    return render(request, 'goTable.html', userInfo)


def boTable(request):
    userInfo = getUserInfo(request)
    return render(request, 'boTable.html', userInfo)


def gsTable(request):
    userInfo = getUserInfo(request)
    return render(request, 'gsTable.html', userInfo)


def bsTable(request):
    userInfo = getUserInfo(request)
    return render(request, 'bsTable.html', userInfo)


def dataAnalysis(request):
    userInfo = getUserInfo(request)
    return render(request, 'dataAnalysis.html', userInfo)


def analysisReport(request):
    userInfo = getUserInfo(request)
    return render(request, 'analysisReport.html', userInfo)
