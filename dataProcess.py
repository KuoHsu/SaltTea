"""
When import action is successful, 
return True, 
otherwise False

Default filename: 
sales.xlsx
purchase.xlsx
salary.xlsx
utility.xlsx

functions:
importSales(username,filaname)
importPurchase(username,filename)
importSalary(username,filename)
importUtility(username,filename)
"""

import pandas as pd
import sys
from fa_system.models import Sales, Purchase, Utility, Salary, CustomUser
from datetime import datetime


def importSales(uid, filename="sales.xlsx"):
    try:

        # sales table
        data = pd.read_excel(filename)

        # 訂單編號(PK)
        salesids = data.loc[6 : len(data) - 2 :][data.columns[0]]

        # 商品編號
        itemids = data.loc[6 : len(data) - 2][data.columns[1]]

        # 商品名稱
        itemnames = data.loc[6 : len(data) - 2][data.columns[2]]

        # 商品種類
        itemgroups = data.loc[6 : len(data) - 2 :][data.columns[3]]

        # 價格
        prices = data.loc[6 : len(data) - 2][data.columns[4]]

        # 數量
        quantities = data.loc[6 : len(data) - 2][data.columns[5]]

        # branch(FK)
        singleBranch = CustomUser.objects.filter(groups__name="branches").get(
            username=uid
        )

        # 日期
        singleDate = data.loc[1][1]
        # 月份
        month = singleDate.month

        for salesid, itemid, itemname, itemgroup, price, quantity in zip(
            salesids, itemids, itemnames, itemgroups, prices, quantities
        ):
            Sales.objects.create(
                # iterable parameter
                salesid=salesid,
                itemid=itemid,
                itemname=itemname,
                itemgroup=itemgroup,
                price=price,
                quantity=quantity,
                # non-iterable parameter
                branch=singleBranch,
                date=singleDate,
                month=month,
            )
        print("Importing successfully")
        return True

    except Exception as e:
        print(str(e), " in line %d" % sys.exc_info()[2].tb_lineno)
        print("Fail to import data")
        return False


def importPurchase(uid, filename="purchase.xlsx"):
    try:
        data = pd.read_excel(filename)

        # 進貨編號(PK)
        # purchaseids=Auto

        # 商品編號
        itemids = data.loc[7 : len(data) - 2 :][data.columns[0]]

        # 商品名稱
        itemnames = data.loc[7 : len(data) - 2 :][data.columns[1]]

        # 價格
        prices = data.loc[7 : len(data) - 2 :][data.columns[2]]

        # 數量
        quantities = data.loc[7 : len(data) - 2 :][data.columns[3]]
        print(uid)
        # 分店(FK)
        singleBranch = CustomUser.objects.filter(groups__name="branches").get(
            username=uid
        )

        # 月份
        singleMonth = data.loc[2][1]

        for itemid, itemname, price, quantity in zip(
            itemids, itemnames, prices, quantities
        ):
            Purchase.objects.create(
                itemid=itemid,
                itemname=itemname,
                branch=singleBranch,
                month=singleMonth,
                price=price,
                quantity=quantity,
            )

        print("Importing successfully")
        return True
    except Exception as e:
        print(str(e), " in line %d" % sys.exc_info()[2].tb_lineno)
        print("Fail to import data")
        return False


def importSalary(uid, filaname="salary.xlsx"):
    try:
        data = pd.read_excel(filaname)

        # 薪資單編號(PK)
        # salaryid=Auto

        # 總額
        singleTotal = data.loc[5][1]

        # branch(FK)
        singleBranch = CustomUser.objects.filter(groups__name="branches").get(
            username=uid
        )

        # 月份
        singleMonth = data.loc[1][1]

        Salary.objects.create(
            branch=singleBranch, month=singleMonth, total=singleTotal
        )

        print("Importing successfully")
        return True

    except Exception as e:
        print(str(e), " in line %d" % sys.exc_info()[2].tb_lineno)
        print("Fail to import data")
        return False


def importUtility(uid, filename="utility.xlsx"):
    try:

        data = pd.read_excel(filename)

        # 帳單編號(PK)
        # billid=Auto

        # branch(FK)
        singleBranch = CustomUser.objects.filter(groups__name="branches").get(
            username=uid
        )

        # 月份
        singleMonth = data.loc[2][1]

        # 電費
        singleEle = data.loc[5][1]

        # 租金
        singleRent = data.loc[4][1]

        Utility.objects.create(
            branch=singleBranch,
            month=singleMonth,
            rent=singleRent,
            electric=singleEle,
        )

        print("Importing successfully")
        return True
    except Exception as e:
        print(str(e), " in line %d" % sys.exc_info()[2].tb_lineno)
        print("Fail to import data")
        return False

