from django.db import models

# Create your models here.
from ekadr import settings


class Field(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name




class Action(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name



class PermissionUserField(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL)
    field = models.ForeignKey(Field)
    def get_PermissionFieldAction(self):
        permissionFieldAction = PermissionFieldAction.objects.filter(permissionfield=self)
        return permissionFieldAction

    # class Meta:
    #     unique_together = (
    #                         ("user", "field","action"),
    #                        # ("user", "extension"),
    #                        # How can I enforce UserProfile's Client
    #                        # and Extension to be unique? This obviously
    #                        # doesn't work, but is this idea possible without
    #                        # creating another FK in my intermediary model
    #                        # ("userprofile__client", "extension")
    #                        )
    def __str__(self):
        return "{}---{}".format(self.user.username,self.field.name)

class PermissionFieldAction(models.Model):
    permissionfield = models.ForeignKey(PermissionUserField)
    action = models.ForeignKey(Action)
    active = models.BooleanField()
    def __str__(self):
        return "{}----{}".format(self.permissionfield.field.name,self.action.name)