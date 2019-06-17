from django.contrib import admin
from fa_system.models import  Investor, Report, Purchase, Sales, Utility, Salary,CustomUser
from django.contrib.auth.admin import UserAdmin



class CustomerUserAdmin(UserAdmin):
    list_display = ('username','name','phone','all_groups')
    fieldsets = (
        ('Profile', {
            'fields': (
                'username',
                'name',
                'email',
                'phone',

            ),
        }),
        ('Permissions',{
            'fields':(
                'is_active',
                'groups',
                'user_permissions'
            )
        }),
    )
   
class InvestorAdmin(admin.ModelAdmin):
    list_display=['investor','number_of_invest']

class ReportAdmin(admin.ModelAdmin):
    list_display=['reportid','analyst','topic','month','path']

class PurchaseAdmin(admin.ModelAdmin):
    list_display=['purchaseid','itemid','itemname','branch','month','price','quantity']

class SalesAdmin(admin.ModelAdmin):
    list_display=['salesid','month','branch','itemid','itemname','itemgroup','price','quantity']

class UtilityAdmin(admin.ModelAdmin):
    list_display=['billid','branch','month','rent','electric']

class SalaryAdmin(admin.ModelAdmin):
    list_display=['salaryid','branch','month','total']
        



admin.site.register(CustomUser,CustomerUserAdmin)
admin.site.register(Investor, InvestorAdmin)#
admin.site.register(Report, ReportAdmin)   
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Sales,SalesAdmin)
admin.site.register(Utility,UtilityAdmin)  
admin.site.register(Salary, SalaryAdmin)

 
