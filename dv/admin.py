from django.contrib import admin

# Register your models here.
from dv.models import *

admin.site.register(Action)
admin.site.register(Field)
admin.site.register(PermissionUserField)
admin.site.register(PermissionFieldAction)