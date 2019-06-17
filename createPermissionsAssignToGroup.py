from django.contrib.auth.models import Permission,Group
from django.contrib.contenttypes.models import ContentType
from fa_system.models import CustomUser

investor=Group.objects.get(name='investors')
branch=Group.objects.get(name='branches')
analyst=Group.objects.get(name='analysts')
finDep=Group.objects.get(name='finDep')


ct=ContentType.objects.get_for_model(CustomUser)
Permission.objects.create(
    codename='asInvestor',
    name='as investor',
    content_type=ct,
)
pInv=Permission.objects.get(name='as investor')

Permission.objects.create(
    codename='asBranch',
    name='as branch',
    content_type=ct,
)
pBra=Permission.objects.get(name='as branch')

Permission.objects.create(
    codename='asAnalyst',
    name='as analyst',
    content_type=ct,
)
pAna=Permission.objects.get(name='as analyst')

Permission.objects.create(
    codename='asFinDep',
    name='as finDep',
    content_type=ct,
)
pFin=Permission.objects.get(name='as finDep')

investor.permissions.add(pInv)
branch.permissions.add(pBra)
analyst.permissions.add(pAna)
finDep.permissions.add(pFin)
print('Done')


