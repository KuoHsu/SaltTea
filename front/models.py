from django.db import models as m

# Create your models here.


class t(m.Model):
    tid = m.TextField(primary_key=True, null=False,
                      max_length=3, default='QQQ')
