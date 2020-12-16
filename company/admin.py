from django.contrib import admin

# Register your models here.
from company.models import *


class BusinnesAdmin(admin.ModelAdmin):
    list_display = ("id","name","parent", )
    list_filter = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('parent',)
    # define the related_lookup_fields
    # related_lookup_fields = {
    #     'fk': ['parent'],
    #     # 'm2m': ['related_m2m'],
    # }
admin.site.register(Businnes,BusinnesAdmin)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id","name", )
    list_filter = ("name",)
    search_fields = ("name",)
    # prepopulated_fields = {'slug': ('title',)}

admin.site.register(Company, CompanyAdmin)

# admin.site.register(Company)

admin.site.register(CompanyProductOrService)

admin.site.register(ProductOrService)
admin.site.register(CompanyAttachment)
