import uuid

from django.db import models

# Create your models here.
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext as _

from payment.models import Order
from payment.models import Event
from geoposition.fields import GeopositionField
from geoposition import Geoposition


class Businnes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey('self',blank=True,null=True)
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255,default='fa fa-sitemap')
    image = models.ImageField('business/images',blank=True,null=True,max_length=500)
    cover = models.ImageField('business/cover',blank=True,null=True,max_length=500)
    order_index = models.IntegerField()
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)
    def __str__(self):
        return self.name
    def get_parent_business(self):
        return Businnes.objects.filter(parent=self).filter(active=True).exclude(id=self.id).order_by('order_index')

    def get_company_count(self):
        return Company.objects.filter(Q(businnes_type=self) | Q(businnes_type__parent=self)).exclude(is_active=False,deleted=True).count()

    def get_own_company_count(self):
        return Company.objects.filter(businnes_type=self).exclude(is_active=False,deleted=True).count()

class Company(models.Model):
    id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='companies/logo',max_length=500)
    cover_photo = models.ImageField(upload_to='companies/cover-photo',blank=True,null=True,max_length=500)
    slogan = models.CharField(max_length=255,blank=True,null=True)
    email = models.EmailField()
    phones = models.CharField(max_length=255,blank=True,null=True)
    voen = models.CharField(max_length=255)
    bank_account = models.CharField(max_length=255) # ayrica cedvelde olmalidir
    region = models.ForeignKey('general.Region')
    address = models.CharField(max_length=255)
    businnes_type = models.ManyToManyField('Businnes')
    is_active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    practices = models.TextField()
    profile = models.ForeignKey('registration.Profile')
    position = GeopositionField(blank=True,null=True)
    slug = models.SlugField(default='slug')
    date = models.DateTimeField(auto_now_add=True)
    def get_company_product_count(self):
        cps = CompanyProductOrService.objects.filter(company=self).filter(active=True).filter(deleted=False).count()
        return cps
    def get_event_count(self):
        ecs = Event.objects.filter(company=self).filter(is_active=True).filter(deleted=False).count()
        return ecs
    def __str__(self):
        return self.name
    def get_attachments(self):
        c_as = CompanyAttachment.objects.filter(company=self)
        return c_as

class CompanyAttachment(models.Model):
    company = models.ForeignKey('Company')
    file = models.FileField(upload_to='company/attachments',max_length=500)
    def __str__(self):
        return self.company.name


ProductOrServiceChoices = (
    ('product', _("product")),
    ('service', _("service")),
)

class CompanyProductOrService(models.Model):
    id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('Company')
    type = models.CharField(max_length=50,choices=ProductOrServiceChoices,default='product')
    product_or_service = models.ForeignKey('ProductOrService')
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='companies/logo',max_length=500)
    slogan = models.CharField(max_length=255,blank=True,null=True)
    quantity = models.DecimalField(max_digits=19, decimal_places=5)
    price = models.DecimalField(max_digits=19, decimal_places=5)
    currency = models.ForeignKey('payment.Currency')
    description = models.TextField()
    businness_types = models.ManyToManyField('Businnes',blank=True,null=True)
    active = models.BooleanField()
    deleted = models.BooleanField(default=False)
    created_date = models.DateField(default=timezone.now())
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name
    def get_company_products_services(self):
        cps = CompanyProductOrService.objects.filter(company=self.company).filter(active=True).filter(deleted=False).exclude(id=self.id)[:13]
        return cps
    def get_images(self):
        cps = CompanyProductOrServiceImage.objects.filter(company_product_or_service=self)
        return cps
    def get_related_products_services(self):
        cps = CompanyProductOrService.objects.filter(product_or_service=self.product_or_service).filter(active=True).filter(deleted=False).exclude(id=self.id)[:13]
        return cps
    def get_order_count(self):
        orders = Order.objects.filter(company_product_or_service=self).filter(active=True)
        quantity = 0
        for order in orders:
            quantity += order.quantity
        return quantity

class CompanyProductOrServiceImage(models.Model):
    company_product_or_service = models.ForeignKey(CompanyProductOrService, default=None)
    image = models.ImageField(upload_to='company_product-or-service/images',
                              verbose_name=_('CompanyProductOrServiceImage') ,max_length=500)

class ProductOrService(models.Model):
    id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    def __str__(self):
        return self.name