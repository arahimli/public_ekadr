from django.contrib import admin

# Register your models here.
from registration.models import *

admin.site.register(Profile)
admin.site.register(ChangeProfileInfo)