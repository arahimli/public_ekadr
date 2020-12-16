from django.db import models

# Create your models here.
class Notification(models.Model):
    profile = models.ForeignKey('registration.Profile')
    # type = models.CharField(max_length=255)
    event = models.ForeignKey('payment.Event',blank=True,null=True)
    company_product_or_service = models.ForeignKey('company.CompanyProductOrService',blank=True,null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.profile.user.username