from django.db import models
from django.utils.translation import ugettext as _
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
# Create your models here.
from ekadr import settings


class CompanyInfo(models.Model): #contact info ayrica cedvelde
    name = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255,blank=True,null=True)
    main_phone = models.CharField(max_length=255,blank=True,null=True)
    main_email = models.EmailField(blank=True,null=True)
    main_address = models.CharField(max_length=255,blank=True,null=True)
    services_about = RichTextUploadingField(blank=True,null=True)
    social_image = models.ImageField('company-info/social-image',blank=True,null=True,max_length=500)
    active = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class UsefulLink(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    new_blank = models.BooleanField(default=False)
    order_index = models.IntegerField()
    active = models.BooleanField()
    def __str__(self):
        return self.title

COLOR_choices = (
    ('fb', _("Facebook_Color")),
    ('tw', _("Twitter_Color")),
    ('googleplus', "Googleplus_Color"),
    ('rss', "Rss_Color"),
    ('pintrest', "Pintrest_Color"),
    ('linkedin', "Linkedin_Color"),
    ('youtube', "Youtube_Color"),
)

class Social(models.Model):
    title = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    color = models.CharField(max_length=255,choices=COLOR_choices)
    url = models.CharField(max_length=255)
    order_index = models.IntegerField()
    active = models.BooleanField()

    def __str__(self):
        return self.title

class Faq(models.Model):
    title = models.CharField(max_length=255)
    context = RichTextUploadingField()
    order_index = models.IntegerField()
    active = models.BooleanField()

    def __str__(self):
        return self.title

class Partner(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='partner',max_length=500)
    url = models.URLField()
    order_index = models.IntegerField()
    active = models.BooleanField()

    def __str__(self):
        return self.name

class Service(models.Model):
    title = models.CharField(max_length=255)
    short_text = models.CharField(max_length=255)
    text = models.TextField(blank=True,null=True)
    icon = models.CharField(max_length=255,blank=True,null=True)
    order_index = models.IntegerField()
    active = models.BooleanField()

    def __str__(self):
        return self.title


class CurrencyDaily(models.Model):
    currency = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=19, decimal_places=5)
    difference = models.DecimalField(max_digits=19, decimal_places=5, blank=True, null=True)
    order_index = models.IntegerField(blank=True)
    # is_active = models.BooleanField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.currency

    class Meta:
        verbose_name_plural = "Valyuta"
        verbose_name = "valyuta"


class Ads(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    home1_ads_name = models.CharField(max_length=255,blank=True,null=True)
    home1_ads_url = models.CharField(max_length=255,blank=True,null=True)
    home1_ads_image = models.ImageField(max_length=500,blank=True,null=True)
    home1_ads_context = models.TextField(blank=True,null=True)
    home1_ads_active = models.BooleanField()
    home2_ads_name = models.CharField(max_length=255,blank=True,null=True)
    home2_ads_url = models.CharField(max_length=255,blank=True,null=True)
    home2_ads_image = models.ImageField(max_length=500,blank=True,null=True)
    home2_ads_context = models.TextField(blank=True,null=True)
    home2_ads_active = models.BooleanField()
    home3_ads_name = models.CharField(max_length=255,blank=True,null=True)
    home3_ads_url = models.CharField(max_length=255,blank=True,null=True)
    home3_ads_image = models.ImageField(max_length=500,blank=True,null=True)
    home3_ads_context = models.TextField(blank=True,null=True)
    home3_ads_active = models.BooleanField()
    home4_ads_name = models.CharField(max_length=255,blank=True,null=True)
    home4_ads_url = models.CharField(max_length=255,blank=True,null=True)
    home4_ads_image = models.ImageField(max_length=500,blank=True,null=True)
    home4_ads_context = models.TextField(blank=True,null=True)
    home4_ads_active = models.BooleanField()
    home5_ads_name = models.CharField(max_length=255,blank=True,null=True)
    home5_ads_url = models.CharField(max_length=255,blank=True,null=True)
    home5_ads_image = models.ImageField(max_length=500,blank=True,null=True)
    home5_ads_context = models.TextField(blank=True,null=True)
    home5_ads_active = models.BooleanField()
    product_detail1_ads_name = models.CharField(max_length=255,blank=True,null=True)
    product_detail1_ads_url = models.CharField(max_length=255,blank=True,null=True)
    product_detail1_ads_image = models.ImageField(max_length=500,blank=True,null=True)
    product_detail1_ads_context = models.TextField(blank=True,null=True)
    product_detail1_ads_active = models.BooleanField(default=False)
    product_detail2_ads_name = models.CharField(max_length=255,blank=True,null=True)
    product_detail2_ads_url = models.CharField(max_length=255,blank=True,null=True)
    product_detail2_ads_image = models.ImageField(max_length=500,blank=True,null=True)
    product_detail2_ads_context = models.TextField(blank=True,null=True)
    product_detail2_ads_active = models.BooleanField(default=False)
    event_detail1_ads_name = models.CharField(max_length=255,blank=True,null=True)
    event_detail1_ads_url = models.CharField(max_length=255,blank=True,null=True)
    event_detail1_ads_image = models.ImageField(max_length=500,blank=True,null=True)
    event_detail1_ads_context = models.TextField(blank=True,null=True)
    event_detail1_ads_active = models.BooleanField(default=False)
    event_detail2_ads_name = models.CharField(max_length=255,blank=True,null=True)
    event_detail2_ads_url = models.CharField(max_length=255,blank=True,null=True)
    event_detail2_ads_image = models.ImageField(max_length=500,blank=True,null=True)
    event_detail2_ads_context = models.TextField(blank=True,null=True)
    event_detail2_ads_active = models.BooleanField(default=False)
    search1_ads_name = models.CharField(max_length=255,blank=True,null=True)
    search1_ads_url = models.CharField(max_length=255,blank=True,null=True)
    search1_ads_image = models.ImageField(max_length=500,blank=True,null=True)
    search1_ads_context = models.TextField(blank=True,null=True)
    search1_ads_active = models.BooleanField(default=False)
    search2_ads_name = models.CharField(max_length=255,blank=True,null=True)
    search2_ads_url = models.CharField(max_length=255,blank=True,null=True)
    search2_ads_image = models.ImageField(max_length=500,blank=True,null=True)
    search2_ads_context = models.TextField(blank=True,null=True)
    search2_ads_active = models.BooleanField(default=False)
    

class AddCart(models.Model):
    company_product_or_service = models.ForeignKey('company.CompanyProductOrService')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    count = models.PositiveIntegerField()
    active = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_product_or_service.name

class WishList(models.Model):
    company_product_or_service = models.ForeignKey('company.CompanyProductOrService')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    active = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_product_or_service.name