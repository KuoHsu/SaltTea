from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)

    def all_groups(self):
        groups = []
        for g in self.groups.all():
            groups.append(g.name)
        return ",".join(groups)

    def __str__(self):
        return self.username


class Investor(models.Model):
    investor = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=True, primary_key=True
    )
    number_of_invest = models.PositiveIntegerField()

    def __str__(self):
        return self.investor


class Report(models.Model):
    reportid = models.AutoField(primary_key=True)
    analyst = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    topic = models.CharField(max_length=100)
    path = models.CharField(max_length=300)
    month = models.PositiveIntegerField()

    def __str__(self):
        return self.analyst


class Purchase(models.Model):
    purchaseid = models.AutoField( primary_key=True)
    itemid = models.CharField(max_length=300)
    itemname = models.CharField(max_length=50)
    branch = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    month = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.purchaseid


class Sales(models.Model):
    salesid = models.CharField(max_length=50, primary_key=True)
    date = models.DateField(auto_now=True)
    branch = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=True)
    itemid = models.CharField(max_length=30)
    itemname = models.CharField(max_length=50)
    itemgroup=models.CharField(max_length=30)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    def __str__(self):
        return self.salesid


class Utility(models.Model):
    billid = models.AutoField(primary_key=True)
    branch = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=True)
    month = models.PositiveIntegerField()
    rent = models.PositiveIntegerField()
    electric = models.PositiveIntegerField()

    def __str__(self):
        return self.billid


class Salary(models.Model):
    salaryid = models.AutoField(primary_key=True)
    branch = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=True)
    month = models.PositiveIntegerField()
    total = models.PositiveIntegerField()

    def __str__(self):
        return self.salaryid

