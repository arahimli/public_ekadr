import datetime
from django.db import models
from django.utils import timezone
from geoposition.fields import GeopositionField
from geoposition import Geoposition


# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=255)
    nominal = models.CharField(max_length=255)
    order_index = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class MonthlyPayment(models.Model): #payment umumi cedvelde olmalidir,heftelik ayliq tipi olmalidir
    profile = models.ForeignKey('registration.Profile')
    price = models.DecimalField(max_digits=19, decimal_places=5)
    currency = models.ForeignKey('Currency')
    is_pay = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.profile.user.username


class Event(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey('company.Company')
    company_product_or_service = models.ForeignKey('company.CompanyProductOrService')
    image = models.ImageField(upload_to='event/image',max_length=500)
    quantity = models.DecimalField(max_digits=19, decimal_places=5)
    price = models.DecimalField(max_digits=19, decimal_places=5,blank=True,null=True)
    currency = models.ForeignKey('Currency')
    is_active = models.BooleanField()
    description = models.TextField()
    businness_types = models.ManyToManyField('company.Businnes',blank=True,null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    position = GeopositionField(blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    def get_appeals(self):
        appeals = EventAppeal.objects.filter(event=self)
        return appeals
    def get_company_events(self):
        events = Event.objects.filter(company=self.company).filter(end_date__lt=timezone.now()).filter(is_active=True,deleted=False).exclude(id=self.id)[:3]
        return events

    def get_related_events(self):
        events = Event.objects.filter(is_active=True,deleted=False).filter(end_date__lt=timezone.now()).exclude(id=self.id).order_by('?')[:4]
        return events

class EventAppeal(models.Model):
    event = models.ForeignKey('Event')
    company = models.ForeignKey('company.Company')
    price = models.DecimalField(max_digits=19, decimal_places=5)
    currency = models.ForeignKey('Currency')
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.event.name
    def get_attachments(self):
        return AttachmentEvent.objects.filter(event_appeal=self)
    class Meta:
        unique_together = ('event', 'company',)
class AttachmentEvent(models.Model):
    event_appeal = models.ForeignKey('EventAppeal')
    file = models.FileField(upload_to='attachments',max_length=500)
    def __str__(self):
        return self.event_appeal.event.name

class EventAppealResult(models.Model):
    event = models.ForeignKey('Event',unique=True)
    eventappeal = models.ForeignKey('EventAppeal')
    is_ative = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    # class Meta:
    #     unique_together = ('event', 'eventappeal',)


class Order(models.Model):
    company_product_or_service = models.ForeignKey('company.CompanyProductOrService')
    quantity = models.DecimalField(max_digits=19, decimal_places=5)
    price = models.DecimalField(max_digits=19, decimal_places=5,blank=True,null=True)
    currency = models.ForeignKey('Currency')
    profile = models.ForeignKey('registration.Profile')
    active = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)