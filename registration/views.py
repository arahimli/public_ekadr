import datetime
import hashlib
import json
import random

from django.template.loader import render_to_string
from django.utils import timezone
import re
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
# from django.shortcuts import render, get_object_or_404


# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _

from ekadr import settings
from registration.forms import *
from registration.models import Profile


def log_out(request):
    if request.user.is_authenticated():
        logout(request)
    next_url = request.GET.get('next_url')
    if next_url:
        pass
    else:
        next_url = reverse('index')
    return HttpResponseRedirect(next_url)


def parent_business_ajax(request):

    context = {
    }
    # return HttpResponse(next_url)
    message = ''
    html_data = ''
    message_code = 0
    continue_op = False
    get_parent_business_html_data = ''
    get_business_html_data = ''
    string_d = ''
    # businnes_types_form = BusinnesTypesForm(request.POST)
    # businnes_types_form.is_valid() = True
    if request.method == 'POST' and request.is_ajax():
        # clean_data = businnes_types_form.cleaned_data
        # business_ids = request.POST['business_ids']
        business_ids = request.POST.getlist('businnes_types')
        businnes_types_parent_ids = request.POST.getlist('businnes_types_parent')
        # print('--------------------------')
        # print(businnes_types_parent_ids)
        # print('--------------------------')
        # for business_id in [business_ids]:
        #     str+=str(business_id)
        business_os = Businnes.objects.filter(id__in=business_ids).filter(parent=None)
        business_parent_os = Businnes.objects.filter(id__in=businnes_types_parent_ids)
        business_parent_os_list = []
        for business_parent_o in business_parent_os:
            business_parent_os_list.append(str(business_parent_o.id))
        selected_for = 0
        general_for = 0
        if business_os:
            try:
                for business_o1 in business_os:
                    if business_o1.get_parent_business():
                        continue_op = True
                        break
                if continue_op:
                    for business_o in business_os:
                        # selected_for = 1
                        if business_o.get_parent_business().count() > 0:
                            for bp in business_o.get_parent_business().all():
                                if str(bp.id) in business_parent_os_list:
                                    active_option = True
                                else:
                                    active_option = False
                                get_parent_business_html_data = '{0}{1}'.format(get_parent_business_html_data,
                                                                                render_to_string(
                                                                                    'include/_html_data/businnes_option.html',
                                                                                    {
                                                                                        'parent_tf': True,
                                                                                        'active_option': active_option,
                                                                                        'bp': bp,
                                                                                        'selected_for': selected_for,
                                                                                        'general_for': general_for,
                                                                                    }))
                                selected_for += 1
                        # get_parent_business_html_data
                        else:
                            pass
                            # selected_for +=1
                            # get_business_html_data = '{0}{1}'.format(get_business_html_data,
                            #                                                 render_to_string(
                            #                                                     'include/_html_data/businnes_option.html',
                            #                                                     {
                            #                                                         'parent_tf': False,
                            #                                                         'business_o': business_o,
                            #                                                     }))
                        # html_data += get_business_html_data

                        # general_for +=1
                    # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                    # print(selected_for)
                    # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                    # print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                    # print(general_for)
                    # print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                    # print('##########################################')
                    # print(business_os.count())
                    # print('##########################################')
                    message_code = 1
                else:
                    message_code = 2
                    html_data = ''
            except:
                message_code = 7
                html_data = ''
        else:
            message_code = 5
            html_data = string_d
    # elif not businnes_types_form.is_valid():
    #     html_data = businnes_types_form

    data = {'message_code': message_code, 'message': get_parent_business_html_data+get_business_html_data}
        # data = {'message_code': message_code, 'message': message}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")




def sign_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard'))
    login_form = LoginForm(request.POST or None, request.FILES or None)
    next_url = request.GET.get('next_url')
    context = {
        'login_form': login_form,
        'next_url': next_url,
    }
    # return HttpResponse(next_url)
    if request.method == 'POST':
        if login_form.is_valid():
            clean_data = login_form.cleaned_data
            username = clean_data.get('username_or_email')
            password = clean_data.get('password')
            remember_me = clean_data.get('remember_me')

            # if remember_me:
            #     remember_me = True
            # else:
            #     remember_me = False

            if '@' in username:
                try:
                    user_email = settings.AUTH_USER_MODEL.objects.get(email=username)
                    user = auth.authenticate(username=user_email.username,
                                             password=password)
                except:
                    user = auth.authenticate(username=username,
                                             password=password)
            else:
                user = auth.authenticate(username=username,
                                         password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    # return HttpResponse(next_url)
                    if next_url =='None' or not next_url:
                        next_url = reverse('index')
                    else:
                        pass
                    # return HttpResponse(next_url)
                    return HttpResponseRedirect(next_url)
                else:
                    message_login = _("please_wait_for_confirmed_account")
            else:
                if '@' in username:
                    message_login = _("email_or_password_incorrect")
                else:
                    message_login = _("username_or_password_incorrect")
            context.update({'message_login':message_login})

            # else:

    return render(request, 'registration/sign_in.html', context=context)



def sign_up(request):
    sign_up_form = SignUpForm(request.POST or None)
    # next_url = request.GET.get('next_url')
    context = {
        # 'next_url': next_url,
    }
    if request.method == 'POST':
        # return HttpResponse(request.POST)
        if sign_up_form.is_valid():
            # return HttpResponse('he')
            clean_data = sign_up_form.cleaned_data
            first_name = clean_data.get('first_name')
            last_name = clean_data.get('last_name')
            username = clean_data.get('username')
            email = clean_data.get('email')
            password = clean_data.get('password')
            type = clean_data.get('type')
            # status = clean_data.get('status')
            status = 'user'
            voen = clean_data.get('voen')
            bank_account = clean_data.get('bank_account')
            region = clean_data.get('region')
            address = clean_data.get('address')
            businnes_types = clean_data.get('businnes_types')
            businnes_types_parent = clean_data.get('businnes_types_parent')
            practices = clean_data.get('practices')
            region_o = Region.objects.filter(id=region).first()
            random_string = str(random.random()).encode('utf8')
            # return HttpResponse(businnes_types_o.count())
            businness_types_o = Businnes.objects.filter(id__in=businnes_types)
            businnes_types_parents_o = Businnes.objects.filter(id__in=businnes_types_parent)
            if businnes_types_parents_o:
                for businnes_types_parent_o in businnes_types_parents_o:
                    if businnes_types_parent_o.parent_id:
                        businness_types_o = businness_types_o.exclude(id=businnes_types_parent_o.parent_id)
            # print('--------------------------')
            # print(businness_types_o.count())
            # # print('--------------------------')
            # print(businnes_types_parents_o.count())
            # return HttpResponse('----------')
            salt = hashlib.sha1(random_string).hexdigest()[:5]

            salted = (salt + email).encode('utf8')

            # activation_key = hashlib.sha1(salted).hexdigest()
            #
            # key_expires = datetime.datetime.today() + datetime.timedelta(1)
            password = make_password(password, salt=salt)
            user = User(first_name=first_name,last_name=last_name,email=email,username=username,password=password,is_active=False,is_staff=False,is_superuser=False)
            user.save()
            if type != 'ordinary-person':
                profile_o = Profile(user=user,type=type,status=status,voen=voen,bank_account=bank_account,region=region_o,address=address,practices=practices)
            else:
                profile_o = Profile(user=user, type=type, status=status,region=region_o)
            for businnes_types_parent_o in businnes_types_parents_o:
                profile_o.businnes_type.add(businnes_types_parent_o)
            for businnes_type_o in businness_types_o:
                profile_o.businnes_type.add(businnes_type_o)
            profile_o.save()
            message_code = 1
            sign_up_form = SignUpForm()
            message = 'succesfully_registered_please_login_to_site'
            context.update({
                'message':message,
                'message_code':message_code,
                'sign_up_form': sign_up_form,
            })
            return render(request, 'registration/sign_up.html', context=context)
        # else:
        #     return HttpResponse('asas')
    context.update({
        'sign_up_form': sign_up_form,
    })
    return render(request, 'registration/sign_up.html', context=context)


def forgot_password(request):
    now = timezone.now()
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard'))
    forgot_password_form = ForgotPasswordForm(request.POST or None)
    if request.method == 'POST':
        # return HttpResponse(request.POST)
        if forgot_password_form.is_valid():
            clean_data = forgot_password_form.cleaned_data
            email = clean_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                pass
            else:
                forgot_password_form._errors['email'] = _('not_user_with_this_email')

    context = {
        'forgot_password_form': forgot_password_form,
        # 'next_url': next_url,
    }
    return render(request, 'registration/forgot_password.html', context=context)

# def forgotPassword_changepassword(request, user_name,activation_key):
#     #check if user is already logged in and if he is redirect him to some other url, e.g. home
#     if request.user.is_authenticated():
#         logout(request)
#
#
#     try:
#         user = User.objects.get(username=user_name)
#     except:
#         raise Http404
#     user_profile = get_object_or_404(Profile,user=user, reset_token_key=activation_key)
#     if user_profile.reset_key_expires > timezone.now():
#         if request.method == 'POST':
#             password = request.POST.get('new-password')
#             password_repeat = request.POST.get('new-password-repeat')
#             if str(password).strip() == str(password_repeat).strip() and len(str(password).strip()) > 7:
#                 if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
#                     user.set_password(password)
#                     user.save()
#                     user_profile.reset_token_key = ''
#                     user_profile.save()
#                     return HttpResponseRedirect('/')
#                 else:
#                     message = 'Password Not Format'
#             elif str(password).strip() != str(password_repeat).strip():
#                 message = 'Passwords not same '
#             else:
#                 if len(str(password).strip()) > 7:
#                     message = 'Password lengt not greater than 8'
#                 else:
#                     message = 'Password Incorrect'
#             context = {
#                     'post_message':message,
#                 }
#             return render(request, 'home/change_password.html', context=context)
#
#             # return HttpResponse('post')
#         return render(request, 'home/change_password.html', context=context)
#
#     else:
#         raise Http404