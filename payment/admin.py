from django.contrib import admin

# Register your models here.
from payment.models import *

admin.site.register(Currency)

admin.site.register(MonthlyPayment)

admin.site.register(Event)

admin.site.register(EventAppeal)

admin.site.register(EventAppealResult)

admin.site.register(Order)

admin.site.register(AttachmentEvent)