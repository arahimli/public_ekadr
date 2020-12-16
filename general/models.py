from django.db import models

# Create your models here.

STATUS_CHOICES = (
    ('married', "Married"),
    ('single', "Single"),
    ('widow', "Widow"),
)
class Region(models.Model):
    parent = models.ForeignKey('self',blank=True,null=True)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    slug = models.SlugField()
    phone_number_code = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
