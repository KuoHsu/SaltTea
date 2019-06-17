from django.shortcuts import render, redirect
from fa_system.models import CustomUser, Purchase, Utility, Salary, Sales
from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse
import dataProcess as dp
from django.contrib.auth.models import Group
from django.db.models import Sum, Max
import pickle
import numpy as np
import json
from sklearn.preprocessing import StandardScaler


# 首頁


def index(request):
    userInfo = get_user_info(request)
    return render(request, "index.html", userInfo)


def product(request):
    return render(request, "product.html")


def about(request):
    return render(request, "about.html")


def data_analysis(request):
    userInfo = get_user_info(request)
    return render(request, 'dataAnalysis.html', userInfo)


def data_analysis_report(request):
    pass


def analysis_report(request):
    userInfo = get_user_info(request)
    return render(request, 'analysisReport.html', userInfo)


# 上傳分析報告
def upload_report_action(request):
    response = HttpResponse()
    if request.method == "POST":

        fileToUpload = request.POST.get("file", None)
        tableType = request.POST.get("reportC", "")
        uploadFlag = True

        response.content = json.dumps({"uploadFlag": uploadFlag})
    return response


# 上傳分析報告頁面
@login_required
@permission_required("fa_system.asBranch")
def upload_report(request):
    return render(request, "uploadReport.html", get_user_info(request))


# 上傳分店報表
@login_required
@permission_required("fa_system.asBranch")
def upload_action(request):

    if (
        request.method == "POST"
        and request.session.get("username", None) != None
    ):
        response = HttpResponse()
        filetype = request.POST.get("category", "")
        uid = request.session.get("username")
        fileToUpload = request.FILES.get("file", "")
        data = dict()

        if filetype == "purchase":
            msg = (
                "Upload successfully"
                if dp.importPurchase(uid, fileToUpload)
                else "Invalid file format"
            )
            data["uploadFlag"] = True
        elif filetype == "sales":
            msg = (
                "Upload successfully"
                if dp.importSales(uid, fileToUpload)
                else "Invalid file format"
            )
            data["uploadFlag"] = True
        elif filetype == "utility":
            msg = (
                "Upload successfully"
                if dp.importUtility(uid, fileToUpload)
                else "Invalid file format"
            )
            data["uploadFlag"] = True
        elif filetype == "salary":
            msg = (
                "Upload successfully"
                if dp.importSalary(uid, fileToUpload)
                else "Invalid file format"
            )
            data["uploadFlag"] = True
        else:
            msg = "您上傳的報表不正確"
            data["uploadFlag"] = False

        data["msg"] = msg
        response.content = json.dumps(data)
        return response

    else:
        return render(request, "uploadReport.html")


# 登入頁面
def login(request):
    return render(request, "login.html")


# 登入
def login_action(request):
    msgToReture = {"message": ""}
    loginFlag = False
    # 確認方法正確
    if request.method == "POST":
        uid = request.POST.get("username", "")
        pwd = request.POST.get("password", "")
        user = auth.authenticate(username=uid, password=pwd)

        if user is not None:
            auth.login(request, user)
            userAs = user.groups.all()[0].name

            # 確認登入身分
            if userAs == "investors":
                request.session["username"] = uid
                request.session["permission"] = "investor"
                loginFlag = True

            elif userAs == "branches":
                request.session["username"] = uid
                request.session["permission"] = "branch"
                loginFlag = True

            elif userAs == "analysts":
                request.session["username"] = uid
                request.session["permission"] = "analyst"
                loginFlag = True

            elif userAs == "finDep":
                request.session["username"] = uid
                request.session["permission"] = "finDep"
                loginFlag = True

            else:
                auth.logout(request)
                loginFlag = False
        request.session["login"] = loginFlag
        response = HttpResponse()
        response.set_cookie("username", uid)
        response.content = json.dumps({"loginFlag": loginFlag})
        return response


# 登出
@login_required
def logout(request):
    print('here')
    # 清除瀏覽器資料

    # 狀態登出
    auth.logout(request)
    return redirect('/index')


# 顯示總體營運報表
def go_table_action(request):
    if request.method == "POST":

        uid = request.session.get("username", None)
        month = request.POST.get("month")

        userInfo = get_user_info(request)

        # 傳回總營運表
        # 銷貨收入
        sales = Sales.objects.filter(month=month)
        price_list = [p.price for p in sales]
        quantity_list = [q.quantity for q in sales]
        sumOfSales = sum([i * j for i, j in zip(price_list, quantity_list)])

        # 銷貨成本
        purchase = Purchase.objects.filter(month=month)
        price_list = [p.price for p in purchase]
        quantity_list = [q.quantity for q in purchase]
        sumOfPurchase = sum([i * j for i, j in zip(price_list, quantity_list)])

        # 租金
        rent = Utility.objects.filter(month=month).aggregate(Sum("rent"))
        rent = 0 if rent['rent__sum'] is None else rent['rent__sum']

        # 電費
        electric = Utility.objects.filter(month=month).aggregate(Sum("electric"))

        electric = 0 if electric['electric__sum'] is None else electric['electric__sum']

        # 薪資
        salary = Salary.objects.filter(month=month).aggregate(Sum("total"))
        salary = 0 if salary['total__sum'] is None else salary['total__sum']

        info = {
            "queryFlag": True,
            "month": month,
            "sales": sumOfSales,
            "costOfSales": sumOfPurchase,
            "rent": rent,
            "salary": salary,
            "electric": electric
        }
        response = HttpResponse()
        response.content = json.dumps(info)
        return response
    else:
        return HttpResponseRedirect("/index/")


# 顯示分店營運報表
def bo_table_action(request):
    if request.method == "POST":

        uid = request.session.get("username", None)
        month = request.POST.get("month")
        branchId = request.POST.get("branchId")
        print(branchId)
        branchIdQuery = int(branchId) - 20000
        userInfo = get_user_info(request)

        # 銷貨收入
        sales = Sales.objects.filter(branch = branchIdQuery).filter(month = month)
        price_list = [p.price for p in sales]
        quantity_list = [q.quantity for q in sales]
        sumOfSales = sum([i * j for i, j in zip(price_list, quantity_list)])

        # 銷貨成本
        purchase = Purchase.objects.filter(
            branch=branchIdQuery).filter(month=month)
        price_list = [p.price for p in purchase]
        quantity_list = [q.quantity for q in purchase]
        sumOfPurchase = sum([i * j for i, j in zip(price_list, quantity_list)])

        # 租金
        rent = Utility.objects.filter(
            branch=branchIdQuery, month=month).aggregate(Sum("rent"))
        rent = 0 if rent['rent__sum'] is None else rent['rent__sum']

        # 電費
        electric = Utility.objects.filter(
            branch=branchIdQuery, month=month).aggregate(Sum("electric"))

        electric = 0 if electric['electric__sum'] is None else electric['electric__sum']

        # 薪資
        salary = Salary.objects.filter(
            branch=branchIdQuery, month=month).aggregate(Sum("total"))
        salary = 0 if salary['total__sum'] is None else salary['total__sum']

        info = {
            "queryFlag": True,
            "branchId": branchId,
            "month": month,
            "sales": sumOfSales,
            "costOfSales": sumOfPurchase,
            "rent": rent,
            "salary": salary,
            "electric": electric
        }
        response = HttpResponse()
        response.content = json.dumps(info)
        return response


# 顯示總體銷售報表
def gs_table_action(request):
    if request.method == "POST":

        uid = request.session.get("username", None)
        month = request.POST.get("month")

        userInfo = get_user_info(request)

        # 傳回總銷售表

        # sales = Sales.objects.filter(month=month)

        # 當月同商品編號合併
        groupedSales = (
            Sales.objects.filter(month=month)
            .values("itemid")
            .annotate(quantity=Sum("quantity"))
            .annotate(price=Max("price"))
            .annotate(itemName=Max("itemname"))
            .annotate(itemGroup=Max("itemgroup"))
        )

        # 處理商品種類
        itemgroup = [int(i["itemGroup"]) for i in groupedSales]
        itemgroupSet = set(itemgroup)
        info = dict()
        for groupId in itemgroupSet:
            info[groupId] = list()

        # 把資料塞進groups裡面
        for item in groupedSales:
            info[int(item["itemGroup"])].append(item)

        response = HttpResponse()
        response.content = json.dumps(
            {
                "queryFlag": True,
                "groups": info,
                "branchId": uid,
                "month": month,
            }
        )
        return response


# 顯示分店銷售報表
def bs_table_action(request):
    if request.method == "POST":

        uid = request.session.get("username", None)
        month = request.POST.get("month")
        branchId = int(request.POST.get("branchId"))
        print(branchId)
        branchIdQuery = branchId - 20000
        userInfo = get_user_info(request)

        # 傳回分店銷售表
        # sales = Sales.objects.filter(month=month).filter(branch=branch)

        # 當月同店家、同商品編號合併
        groupedSales = (
            Sales.objects.filter(month = month, branch = branchIdQuery)
            .values("itemid")
            .annotate(quantity=Sum("quantity"))
            .annotate(price=Max("price"))
            .annotate(itemName=Max("itemname"))
            .annotate(itemGroup=Max("itemgroup"))
        )
        # 處理商品種類
        itemgroup = [int(i["itemGroup"]) for i in groupedSales]
        itemgroupSet = set(itemgroup)
        info = dict()
        for groupId in itemgroupSet:
            info[groupId] = list()

        # 把資料塞進groups裡面
        for item in groupedSales:
            info[int(item["itemGroup"])].append(item)

        response = HttpResponse()
        response.content = json.dumps(
            {
                "queryFlag": True,
                "groups": info,
                "branchId": branchId,
                "month": month,
            }
        )
        print(response.content)
        return response


# 總營運報表頁面
def go_table(request):
    userInfo = get_user_info(request)
    return render(request, 'goTable.html', userInfo)

# 分店營運報表頁面


def bo_table(request):
    info = get_user_info(request)
    permission = request.session.get("permission", None)
    ids = list()
    ids.append(request.session.get("username", None))
    uids = ids\
            if permission == 'branch'\
            else [u.username for u in CustomUser.objects.filter(username__startswith='2')] 
    info['branchIds'] = uids
    return render(request, 'boTable.html', info)

# 總銷售報表頁面


def gs_table(request):
    userInfo = get_user_info(request)
    return render(request, 'gsTable.html', userInfo)

# 分店銷售報表頁面


def bs_table(request):
    info = get_user_info(request)
    permission = request.session.get("permission", None)
    ids = list()
    ids.append(request.session.get("username", None))
    uids = ids\
        if permission == 'branch'\
        else [u.username for u in CustomUser.objects.filter(username__startswith='2')]
    print(uids)
    info['branchIds'] = uids
    print(info)
    return render(request, 'bsTable.html', info)


# tools
def get_user_info(request):
    r = dict()
    r["login"] = request.session.get("login", False)
    r["username"] = request.session.get("username", "")
    r["permission"] = request.session.get("permission", "guest")
    return r


@permission_required("fa_system.analysts")
def data_analysis_query(request):
# 給 month 傳回 x,y


    if request.method == "POST":

        month = request.POST.get("month")

        userInfo = get_user_info(request)

        # 初始化七筆輸入資料
        months = []
        saleses = []
        salarys = []
        purchases = []
        rents = []
        electrics = []

        # 取前六個月的月份和本月，遞增排序
        for i in range(6, -1, -1):
            thisMonth = (month - i) if (month - i) > 0 else (month - i) + 12
            months.append(thisMonth)

            # 銷貨收入
            sales = Sales.objects.filter(month=thisMonth)
            price_list = [p.price for p in sales]
            quantity_list = [q.quantity for q in sales]
            saleses.append(
                sum([i * j for i, j in zip(price_list, quantity_list)])
            )

            # 薪資
            salarys.append(
                Salary.objects.filter(month=thisMonth).aggregate(
                    salary=Sum("total")
                )["salary"]
            )

            # 銷貨成本
            purchase = Purchase.objects.filter(month=thisMonth)
            price_list = [p.price for p in purchase]
            quantity_list = [q.quantity for q in purchase]
            purchases.append(
                sum([i * j for i, j in zip(price_list, quantity_list)])
            )

            # 電費
            electrics.append(
                Utility.objects.filter(month=thisMonth).aggregate(
                    electric=Sum("electric")
                )["electric"]
            )

            # 租金
            rents.append(
                Utility.objects.filter(month=thisMonth).aggregate(
                    rent=Sum("rent")
                )["rent"]
            )

        x = []
        for m, s1, s2, p, e, r in zip(
            months, saleses, salarys, purchases, electrics, rents
        ):
            x.append([m, s1, s2, p, e, r])

        # 標準化輸入變數
        x = np.array(np.float64(x))
        # meanList=
        # sdList=
        # x_sd=(x-meanList)/sdList

        # 取得預測模型
        with open("./svrModel.pickle", "rb") as f: 
                predictModel = pickle.load(f) 


        sd_x = StandardScaler()

        x = sd_x.fit_transform(x)

        y_pred = predictModel.predict(x)
        info={
            'x':months,
            'y':y_pred
        }
        response = HttpResponse()
        response.content = info
        return render(request, "dataAnalysis.html", info)


# backup


# def showTable(request):
#     if request.method == "POST":

#         uid = request.session.get("username", None)
#         month = request.POST.get("month")
#         tableType = request.POST.get("tableType")

#         userInfo = getUserInfo(request)

#         # 傳回總營運表
#         if tableType == "goTable":

#             # 銷貨收入
#             sales = Sales.objects.filter(month=month)
#             price_list = [p.price for p in sales]
#             quantity_list = [q.quantity for q in sales]
#             sumOfSales = sum(
#                 [i * j for i, j in zip(price_list, quantity_list)]
#             )

#             # 銷貨成本
#             purchase = Purchase.objects.filter(month=month)
#             price_list = [p.price for p in purchase]
#             quantity_list = [q.quantity for q in purchase]
#             sumOfPurchase = sum(
#                 [i * j for i, j in zip(price_list, quantity_list)]
#             )

#             # 租金
#             rent = Utility.objects.filter(month=month).aggregate(Sum("rent"))

#             # 電費
#             electric = Utility.objects.filter(month=month).aggregate(
#                 Sum("electric")
#             )

#             # 薪資
#             salary = Salary.objects.get(month=month).aggregate(Sum("total"))

#             info = {
#                 "month": month,
#                 "sales": sumOfSales,
#                 "costOfSales": sumOfPurchase,
#                 "rent": rent,
#                 "salary": salary,
#                 "electric": electric,
#             }

#             response = HttpResponse()
#             response.content = json.dumps({"loginFlag": True, "groups": info})
#             return response

#         # 傳回分店營運表
#         elif tableType == "boTable":
#             branch = CustomUser.objects.get(username=uid)

#             # 銷貨收入
#             sales = Sales.objects.filter(branch=branch).filter(month=month)
#             price_list = [p.price for p in sales]
#             quantity_list = [q.quantity for q in sales]
#             sumOfSales = sum(
#                 [i * j for i, j in zip(price_list, quantity_list)]
#             )

#             # 銷貨成本
#             purchase = Purchase.objects.filter(branch=branch).filter(
#                 month=month
#             )
#             price_list = [p.price for p in purchase]
#             quantity_list = [q.quantity for q in purchase]
#             sumOfPurchase = sum(
#                 [i * j for i, j in zip(price_list, quantity_list)]
#             )

#             # 租金
#             rent = Utility.objects.get(branch=branch, month=month).rent

#             # 電費
#             electric = Utility.objects.get(branch=branch, month=month).electric

#             # 薪資
#             salary = Salary.objects.get(branch=branch, month=month).total

#             info = {
#                 "branchId": uid,
#                 "month": month,
#                 "sales": sumOfSales,
#                 "costOfSales": sumOfPurchase,
#                 "rent": rent,
#                 "salary": salary,
#                 "electric": electric,
#             }
#             response = HttpResponse()
#             response.content = json.dumps({"loginFlag": True, "groups": info})
#             return response

#         # 傳回總銷售表
#         elif tableType == "gsTable":

#             # sales = Sales.objects.filter(month=month)

#             # 當月同商品編號合併
#             groupedSales = (
#                 Sales.objects.filter(month=month)
#                 .values("itemid")
#                 .annotate(quantity=Sum("quantity"))
#                 .annotate(price=Max("price"))
#                 .annotate(itemname=Max("itemname"))
#                 .annotate(itemgroup=Max("itemgroup"))
#             )

#             # 處理商品種類
#             itemgroup = [int(i["itemgroup"]) for i in groupedSales]
#             itemgroupSet = set(itemgroup)
#             info = dict()
#             for groupId in itemgroupSet:
#                 info[groupId] = list()

#             # 把資料塞進groups裡面
#             for item in groupedSales:
#                 info[int(item["itemgroup"])].append(item)

#             response = HttpResponse()
#             response.content = json.dumps({"loginFlag": True, "groups": info})
#             return response

#         # 傳回分店銷售表
#         elif tableType == "bsTable":
#             # sales = Sales.objects.filter(month=month).filter(branch=branch)

#             # 當月同店家、同商品編號合併
#             groupedSales = (
#                 Sales.objects.filter(month=month, branch=branch)
#                 .values("itemid")
#                 .annotate(quantity=Sum("quantity"))
#                 .annotate(price=Max("price"))
#                 .annotate(itemname=Max("itemname"))
#                 .annotate(itemgroup=Max("itemgroup"))
#             )
#             # 處理商品種類
#             itemgroup = [int(i["itemgroup"]) for i in groupedSales]
#             itemgroupSet = set(itemgroup)
#             info = dict()
#             for groupId in itemgroupSet:
#                 info[groupId] = list()

#             # 把資料塞進groups裡面
#             for item in groupedSales:
#                 info[int(item["itemgroup"])].append(item)

#             response = HttpResponse()
#             response.content = json.dumps({"loginFlag": True, "groups": info})
#             return response

#         else:
#             return HttpResponseRedirect("/index/")

#     else:
#         return HttpResponseRedirect("/index/")
