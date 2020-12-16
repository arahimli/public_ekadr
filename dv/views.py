from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from dv.models import *


def index(request):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    actions = Action.objects.all()
    fields = Field.objects.all()
    permissions = PermissionUserField.objects.filter(user=user)
    permission_actions = PermissionFieldAction.objects.filter(permissionfield__user=user)
    list = []
    if request.method == 'POST':
        data_p = request.POST
        # return HttpResponse(request.POST)
        for permission in permissions:
            list_action = []
            for permission_action in permission.get_PermissionFieldAction():
                filed =  False
                # return HttpResponse(list_action)
                if data_p.get('field_'+str(permission.field.id) + '_' + str(permission_action.action.id)) == 'on':
                    filed = True
                # list_action.append(filed)
                permission_action.active = filed
                permission_action.save()
            # return HttpResponse(list_action)
    # for field in fields:
    #     if PermissionField.objects.filter(user=user,field=field):
    #         pf = PermissionField(user=user,field=field)
    #         pf.save()
    # # tourpackeges = None
    # for pf_o in PermissionField.objects.filter(user=user):
    #     for action in actions:
    #         pfa = PermissionFieldAction(permissionfield=pf_o,action=action,active=False)
    #         pfa.save()
    context = {
        'fields':fields,
        'actions':actions,
        'permissions':permissions,
        'permission_actions':permission_actions,
    }
    # return HttpResponse('salam')
    return render(request, 'dv/index.html', context=context)
