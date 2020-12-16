import uuid

from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.
# from company import models
from company.models import Company
from ekadr import settings
from userprofile.models import Notification
from django.utils import timezone

STATUS_CHOICES = (
    ('married', _("Married")),
    ('single', _("Single")),
    ('widow', _("Widow")),
)
TYPECHOICES = (
    ('juridical-person', _("juridical_person")),
    ('individual-person', _("individual_person")),
    ('ordinary-person', _("ordinary_person")),
)

ONLYADMINTYPECHOICES = (
    ('admin-person', _("admin_person")),
)

ADMINTYPECHOICES = (
    ('admin-person', _("admin_person")),
    ('juridical-person', _("juridical_person")),
    ('individual-person', _("individual_person")),
    ('ordinary-person', _("ordinary_person")),
)

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    image = models.ImageField(upload_to='profile_photos',blank=True,null=True,max_length=500)
    type = models.CharField(max_length=100,choices=ADMINTYPECHOICES,default='juridical-person')
    status = models.CharField(max_length=100,choices=STATUS_CHOICES,blank=True,null=True)
    voen = models.CharField(max_length=255,blank=True)
    bank_account = models.CharField(max_length=255,blank=True) # ayrcia cedvelde olmalidir
    region = models.ForeignKey('general.Region')
    address = models.TextField(blank=True)
    businnes_type = models.ManyToManyField('company.Businnes')
    practices = models.TextField(blank=True,null=True)
    activation_key = models.CharField(max_length=40, blank=True,editable=False)
    reset_token_key = models.CharField(max_length=40, blank=True,editable=False)
    key_expires = models.DateTimeField(default=timezone.now(),blank=True,null=True,editable=False)
    reset_key_expires = models.DateTimeField(default=timezone.now(), blank=True, null=True,editable=False)
    def __str__(self):
        return self.user.username
    def get_companies(self):
        companies = Company.objects.filter(profile=self).filter(deleted=False)
        return companies
    def get_notifications(self):
        notifications = Notification.objects.filter(profile=self).order_by('-date')[:7]
        return notifications

class ChangeProfileInfo(models.Model):
    profile = models.ForeignKey('Profile')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    type = models.CharField(max_length=100,choices=TYPECHOICES,default='juridical-person')
    voen = models.CharField(max_length=255)
    bank_account = models.CharField(max_length=255)
    region = models.ForeignKey('general.Region')
    address = models.CharField(max_length=255)
    businnes_type = models.ManyToManyField('company.Businnes',blank=True,null=True)
    practices = models.TextField(blank=True,null=True)
    admin_confirm = models.BooleanField(default=False)
    admin_reject = models.BooleanField(default=False)
    email_confirm = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    # active = models.BooleanField()
    # def __str__(self):
    #     return self.profile.user.username
