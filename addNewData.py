from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from fa_system.models import Investor, Report, Purchase, Sales, Utility, CustomUser, Salary
from django.contrib.auth import get_user_model
import math
import random
import pandas as pd

user = CustomUser.objects.filter(groups__name='branches')[0]


dataSalary = pd.read_excel('Salary.xlsx')

for i in range(0, len(dataSalary)):
    Salary.objects.create(branch=user,
                          month=dataSalary.loc[i][2],
                          total=dataSalary.loc[i][3],
                          )

dataPurchase = pd.read_excel('Purchase.xlsx')

for j in range(0, len(dataPurchase)):
    Purchase.objects.create(itemid=dataPurchase.loc[j][1],
                            itemname=dataPurchase.loc[j][4],
                            branch=user,
                            month=dataPurchase.loc[j][3],
                            price=dataPurchase.loc[j][5],
                            quantity=dataPurchase.loc[j][6],
                            )

dataSales = pd.read_excel('Sales.xlsx')

for k in range(0, len(dataSales)):
    Sales.objects.create(salesid=dataSales.loc[k][0],
                         date=dataSales.loc[k][1],
                         branch=user,
                         itemid=dataSales.loc[k][3],
                         itemname=dataSales.loc[k][4],
                         itemgroup=dataSales.loc[k][7],
                         price=dataSales.loc[k][5],
                         quantity=dataSales.loc[k][6],
                         month=dataSales.loc[k][8],
                         )

dataUtility = pd.read_excel('Utility.xlsx')

for l in range(0, len(dataUtility)):
    Utility.objects.create(branch=user,
                           month=dataSales.loc[l][2],
                           rent=dataSales.loc[l][3],
                           electric=dataSales.loc[l][4],
                           )
