import profile

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from flynsarmy_paginator.paginator import FlynsarmyPaginator
# Create your views here.
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.utils.translation import ugettext as _
# from numpy.core.defchararray import lower
# from wagtail.wagtailimages.templatetags.wagtailimages_tags import image
from django.db.models import Q
import company
from company.models import *
from home.models import AddCart
from payment.models import *
from registration.models import *
from general.models import *
from userprofile.forms import *
from userprofile.models import Notification
from geoposition import Geoposition


@login_required(login_url='sign_in')
def dashboard(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    # tourpackeges = None
    context = {}
    now = timezone.now()

    if profile.type == 'admin-person':
        default_year = 2017
        chart_type = {}
        business_o = Businnes.objects.filter(active=True).order_by('order_index').filter(parent=None).first()
        business_year_list = []
        if int(now.year) == default_year:
            business_year_list.append(default_year)
        else:
            if int(now.year) - default_year < 11:
                for x in range(default_year, now.year + 1):
                    business_year_list.append(x)
            else:
                for x in range(int(now.year) - 10, int(now.year + 1)):
                    business_year_list.append(x)
        selected_for = 0
        general_for = 0
        data_list = []
        if business_o:
            try:
                main_business = business_o
                # print('=======================================')
                # print(business_o.name)
                # print('=======================================')
                for business_year_list_item in business_year_list:
                    data_list.append(
                        {
                            'year': business_year_list_item,
                            'main_business': main_business,
                            'company_count': Company.objects.filter(businnes_type=main_business).filter(
                                date__year=business_year_list_item).count(),
                            'event_count': Event.objects.filter(businness_types=main_business).filter(
                                date__year=business_year_list_item).count(),
                            'pors_count': CompanyProductOrService.objects.filter(businness_types=main_business).filter(
                                date__year=business_year_list_item).count(),
                        }
                    )
            except:
                pass

        companies_now = Company.objects.filter(deleted=False).filter(date__year=now.year)
        pors_now = CompanyProductOrService.objects.filter(deleted=False).filter(date__year=now.year)
        events_now = Event.objects.filter(deleted=False).filter(date__year=now.year)
        month_list = [
            {'num': 1, 'name': _('january')},
            {'num': 2, 'name': _('february')},
            {'num': 3, 'name': _('march')},
            {'num': 4, 'name': _('april')},
            {'num': 5, 'name': _('may')},
            {'num': 6, 'name': _('june')},
            {'num': 7, 'name': _('july')},
            {'num': 8, 'name': _('august')},
            {'num': 9, 'name': _('september')},
            {'num': 10, 'name': _('october')},
            {'num': 11, 'name': _('november')},
            {'num': 12, 'name': _('december')},
        ]
        data_list_month = []
        for month_list_item in month_list:
            data_list_month.append(
                {
                    "month_format": "{:0>2d}".format(month_list_item['num']),
                    "month": month_list_item['num'],
                    "month_name": month_list_item['name'],
                    "company_count": companies_now.filter(date__month=month_list_item['num']).count(),
                    "pors_count": pors_now.filter(date__month=month_list_item['num']).count(),
                    "event_count": events_now.filter(date__month=month_list_item['num']).count(),
                }
            )
        # chart_type['data_list_month'] = data_list_month
        # print(chart_type['data_list_month'])
        chart_type['juridical_person'] = Profile.objects.filter(type='juridical-person').count()
        chart_type['individual_person'] = Profile.objects.filter(type='individual-person').count()
        chart_type['ordinary_person'] = Profile.objects.filter(type='ordinary-person').count()
        chart_type['admin_person'] = Profile.objects.filter(type='admin-person').count()
        businnes_type_form = BusinnesTypeForm(request.POST or None)
        businnes_type_year_form = BusinnesTypeYearForm(request.POST or None)
        context.update({
            'chart_type': chart_type,
            'businnes_type_form': businnes_type_form,
            'businnes_type_year_form': businnes_type_year_form,
            'data_list': data_list,
            'data_list_month': data_list_month
        })

        # return HttpResponse(context.items())
    companies = Company.objects.filter(profile=profile).filter(deleted=False)[:3]
    company_products_or_services = CompanyProductOrService.objects.filter(company__profile=profile).filter(
        deleted=False)[:12]
    # return HttpResponse(company_products_or_services.count())
    context.update({
        'companies': companies,
        'company_product_or_services': company_products_or_services,
    })
    return render(request, 'profile/dashboard.html', context=context)

@login_required(login_url='sign_in')
def company_product_or_service_preview(request, cp_id):
    # now = timezone.now()
    company_product_or_service = get_object_or_404(CompanyProductOrService, ~Q(company__deleted=True),
                                                   ~Q(company__is_active=False), id=cp_id, deleted=False)
    # tourpackeges = None
    # .filter(start_date__gte=now).filter(end_date__lte=now)[:18]
    context = {
        'company_product_or_service': company_product_or_service,
    }
    return render(request, 'company/product_or_service.html', context=context)

@login_required(login_url='sign_in')
def profile_wish_list(request):
    # now = timezone.now()
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    order_list = AddCart.objects.filter(user=user)
    # company_product_or_service_list = CompanyProductOrService.objects.filter(deleted=False)
    # .filter(start_date__gte=now).filter(end_date__lte=now)[:18]
    # contact_list = Contacts.objects.all()
    paginator = FlynsarmyPaginator(order_list, 30, adjacent_pages=3)  # Show 25 contacts per page

    page = request.GET.get('page')  # page check is tam eded
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        orders = paginator.page(paginator.num_pages)
    context = {
        # 'company': company,
        # 'ImageFormSet': ImageFormSet,
        'orders': orders,
    }
    return render(request, 'profile/ordinary/wish_list.html', context=context)

@login_required(login_url='sign_in')
def profile_products_buy_list(request):
    # now = timezone.now()
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    order_list = Order.objects.filter(profile=user_profile)
    # company_product_or_service_list = CompanyProductOrService.objects.filter(deleted=False)
    # .filter(start_date__gte=now).filter(end_date__lte=now)[:18]
    # contact_list = Contacts.objects.all()
    paginator = FlynsarmyPaginator(order_list, 30, adjacent_pages=3)  # Show 25 contacts per page

    page = request.GET.get('page')  # page check is tam eded
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        orders = paginator.page(paginator.num_pages)
    context = {
        # 'company': company,
        # 'ImageFormSet': ImageFormSet,
        'orders': orders,
    }
    return render(request, 'profile/ordinary/products_buy_list.html', context=context)


@login_required(login_url='sign_in')
def admin_details_data_change_section(request, content_slug):
    user = request.user
    all_data = None
    profile = get_object_or_404(Profile, user=user, type='admin-person')
    search_word = request.GET.get('search')
    # if content_slug == 'companies':
    if content_slug == 'profiles':
        data_list = ChangeProfileInfo.objects.filter(email_confirm=True,admin_confirm=False,admin_reject=False).order_by('-date')
        if search_word:
            data_list = data_list.filter(Q(user__first_name=search_word) | Q(user__last_name=search_word) | Q(user__email__icontains=search_word) | Q(voen__icontains=search_word) | Q(bank_account__icontains=search_word))
    else:
        raise Http404
    paginator = FlynsarmyPaginator(data_list, 50, adjacent_pages=2)  # Show 25 contacts per page
    # print(all_data.count())
    page = request.GET.get('page')  # check tam eded
    # print(page)
    page = 1
    try:
        all_data = paginator.page(page)
        # print(datas)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        all_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        all_data = paginator.page(paginator.num_pages)
    # return HttpResponse(str(datas.count()))
    # tourpackeges = None
    # return HttpResponse(company_products_or_services.count())
    context = {
        'content_slug': content_slug,
        'datas': all_data,
        'search_word': search_word,
    }
    return render(request, 'profile/admin/confirm_changes_list.html', context=context)



@login_required(login_url='sign_in')
def admin_profile_details_changed_data_confirm(request, content_slug, p_id):
    user = request.user
    all_data = None
    profile = get_object_or_404(Profile, user=user, type='admin-person')
    profile_changed_o = get_object_or_404(ChangeProfileInfo, ~Q(profile__type='admin-person'), profile__id=p_id,admin_confirm=False,admin_reject=False)
    profile_o = get_object_or_404(Profile, ~Q(type='admin-person'), id=p_id)
    form = AdminConfirmRejectedProfileConfirm(request.POST or None, request.FILES or None)
    context = {
        'content_slug': content_slug,
        'profile_changed_o': profile_changed_o,
        'profile_o': profile_o,
        'admin_profile_form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            clean_data = form.cleaned_data
            is_confirm = clean_data.get('is_confirm')
            if is_confirm == 'confirm':
                profile_o.user.first_name = profile_changed_o.first_name
                profile_o.user.last_name = profile_changed_o.last_name
                profile_o.voen = profile_changed_o.voen
                profile_o.bank_account = profile_changed_o.bank_account
                profile_o.region = profile_changed_o.region
                profile_o.address= profile_changed_o.address
                profile_o.practices= profile_changed_o.practices
                profile_o.type= profile_changed_o.type
                profile_o.save()
                profile_o.user.save()
                profile_changed_o.admin_confirm = True
                profile_changed_o.save()
            elif is_confirm == 'reject':
                profile_changed_o.admin_reject = True
                profile_changed_o.save()
            else:
                pass
            url = reverse('admin_details_data_change_section', kwargs={'content_slug': 'profiles'})
            return HttpResponseRedirect(url)

    return render(request, 'profile/admin/confirm_changes.html', context=context)




@login_required(login_url='sign_in')
def admin_content_section(request, content_slug, a_slug):
    user = request.user
    all_data = None
    profile = get_object_or_404(Profile, user=user, type='admin-person')
    search_word = request.GET.get('search')
    if content_slug == 'companies':
        if a_slug == 'all':
            data_list = Company.objects.filter(deleted=False)
            # return HttpResponse(data_list.count())
        elif a_slug == 'active':
            data_list = Company.objects.filter(deleted=False).filter(is_active=True).order_by('-date')
        elif a_slug == 'deactive':
            data_list = Company.objects.filter(deleted=False).filter(is_active=False).order_by('-date')
        else:
            raise Http404
        if search_word:
            # return HttpResponse('sasaskj')
            data_list = data_list.filter(Q(name__icontains=search_word) | Q(slogan__icontains=search_word) | Q(email__icontains=search_word) | Q(phones__icontains=search_word) | Q(voen__icontains=search_word) | Q(bank_account__icontains=search_word))
            # return  HttpResponse(data_list.count())
    elif content_slug == 'profiles':
        if a_slug == 'all':
            data_list = Profile.objects.filter(~Q(type='admin-person'))
        elif a_slug == 'active':
            data_list = Profile.objects.filter(~Q(type='admin-person')).filter(user__is_active=True)
        elif a_slug == 'deactive':
            data_list = Profile.objects.filter(~Q(type='admin-person')).filter(user__is_active=False)
        else:
            raise Http404
        if search_word:
            data_list = data_list.filter(Q(user__first_name=search_word) | Q(user__last_name=search_word) | Q(user__email__icontains=search_word) | Q(voen__icontains=search_word) | Q(bank_account__icontains=search_word))
    else:
        raise Http404
    # print(data_list)
    # paginator = Paginator(data_list, 25) # Show 25 contacts per page
    #
    # page = request.GET.get('page')
    # try:
    #     all_data = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     all_data = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     all_data = paginator.page(paginator.num_pages)
    paginator = FlynsarmyPaginator(data_list, 50, adjacent_pages=2)  # Show 25 contacts per page
    # print(all_data.count())
    page = request.GET.get('page')  # check tam eded
    # print(page)
    page = 1
    try:
        all_data = paginator.page(page)
        # print(datas)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        all_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        all_data = paginator.page(paginator.num_pages)
    # return HttpResponse(str(datas.count()))
    # tourpackeges = None
    # return HttpResponse(company_products_or_services.count())
    context = {
        'content_slug': content_slug,
        'datas': all_data,
        'search_word': search_word,
    }
    return render(request, 'profile/admin/admin-contents.html', context=context)


@login_required(login_url='sign_in')
def admin_company_page(request, content_slug, c_id):
    company_o = get_object_or_404(Company, id=c_id, deleted=False)
    form = AdminCompanyConfirm(request.POST or None, request.FILES or None, initial={
        'is_active': company_o.is_active
    })
    context = {
        'content_slug': content_slug,
        'company': company_o,
        'admin_company_form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            clean_data = form.cleaned_data
            is_active = clean_data.get('is_active')
            if is_active:
                is_active = True
            else:
                is_active = False
            company_o.is_active = is_active
            company_o.save()
            success_messages = 'company_activated_successfully'
            context.update({
                'success_messages': success_messages,
            })

    return render(request, 'profile/admin/admincompany_page.html', context=context)


@login_required(login_url='sign_in')
def admin_profile_page(request, content_slug, p_id):
    user = request.user
    all_data = None
    profile = get_object_or_404(Profile, user=user, type='admin-person')
    profile_o = get_object_or_404(Profile, ~Q(type='admin-person'), id=p_id)
    form = AdminProfileConfirm(request.POST or None, request.FILES or None, initial={
        'is_active': profile_o.user.is_active
    })
    context = {
        'content_slug': content_slug,
        'profile_o': profile_o,
        'admin_profile_form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            clean_data = form.cleaned_data
            is_active = clean_data.get('is_active')
            if is_active:
                is_active = True
            else:
                is_active = False
            profile_o.user.is_active = is_active
            profile_o.user.save()
            success_messages = _('profile_activated_successfully')
            context.update({
                'success_messages': success_messages,
            })

    return render(request, 'profile/admin/admin_profile_page.html', context=context)


@login_required(login_url='sign_in')
def my_companies(request):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    # tourpackeges = None
    companies = Company.objects.filter(profile=profile).filter(deleted=False)
    messages_spec = request.GET.get('messages')

    context = {
        'profile': profile,
        'companies': companies,
    }
    if messages_spec:
        context.update({
            'messages_spec':messages_spec
        })
    return render(request, 'profile/my_companies.html', context=context)


@login_required(login_url='sign_in')
def my_company(request, c_id):
    user = request.user
    profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'),
                                user=user)  # compamy eventler ucun tekrar sorgu getmemesi ucun
    company = get_object_or_404(Company, profile=profile, id=c_id)
    company_product_or_service_list = CompanyProductOrService.objects.filter(company=company).filter(deleted=False)
    paginator = FlynsarmyPaginator(company_product_or_service_list, 25, adjacent_pages=4)  # Show 25 contacts per page

    page = request.GET.get('page')  # check tam eded
    try:
        company_products_or_services = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        company_products_or_services = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        company_products_or_services = paginator.page(paginator.num_pages)
    url = request.path
    messages = request.GET.get('messages')
    # return HttpResponse(url)
    # return HttpResponse(company.id)
    context = {
        'company': company,
        'messages': messages,
        'company_product_or_service_count': company_product_or_service_list.count(),
        'company_events_count': Event.objects.filter(company=company).filter(deleted=False).count(),
        'url': url,
        'company_products_or_servicess': company_products_or_services,
    }
    return render(request, 'profile/my_company.html', context=context)


@login_required(login_url='sign_in')
def my_company_products(request):
    # tourpackeges = TourPackage.objects.all()
    # tourpackeges = None
    context = {
        # 'tourpackeges':tourpackeges,
    }
    return render(request, 'profile/dashboard.html', context=context)


@login_required(login_url='sign_in')
def my_company_product(request):
    # tourpackeges = TourPackage.objects.all()
    # tourpackeges = None
    context = {
        # 'tourpackeges':tourpackeges,
    }
    return render(request, 'profile/dashboard.html', context=context)


@login_required(login_url='sign_in')
def recycle_bin(request, content_slug):
    user = request.user
    profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    if content_slug == 'products-or-services':
        data_list = CompanyProductOrService.objects.filter(company__profile=profile).filter(deleted=True)
    elif content_slug == 'companies':
        data_list = Company.objects.filter(profile=profile).filter(deleted=True)
    elif content_slug == 'events':
        data_list = Event.objects.filter(company__profile=profile).filter(deleted=True)
    else:
        raise Http404
    paginator = FlynsarmyPaginator(data_list, 25, adjacent_pages=4)  # Show 25 contacts per page

    page = request.GET.get('page')  # check tam eded
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        datas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        datas = paginator.page(paginator.num_pages)
    # return HttpResponse('dsdsd23')
    context = {
        'datas': datas,
        'content_slug': content_slug,
    }
    return render(request, 'profile/recycle_bin.html', context=context)


@login_required(login_url='sign_in')
def product_service_redirect(request, action_slug):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    user_profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    my_companies = Company.objects.filter(profile=user_profile).filter(is_active=True,
                                                                       deleted=False)  # compamyler ucun tekrar sorgu getmemesi ucun
    if action_slug == 'list':
        template_name = 'profile/product_or_service/list_product_service_redirect.html'
        # return HttpResponse(template_name)
    elif action_slug == 'create':
        template_name = 'profile/product_or_service/create_product_service_redirect.html'
    else:
        raise Http404
    # url = reverse('create_product_service', kwargs={'company_id': my_companies.first().id})
    # return HttpResponse(url)
    # if my_companies.count() == 1:
    #     url = reverse('create_product_service', kwargs={'company_id': my_companies.first().id})
    #     return HttpResponseRedirect(url)
    context = {
        'companies': my_companies,
    }

    # return  HttpResponse(template_name)
    return render(request, template_name, context=context)


# @login_required(login_url='sign_in')
# def list_product_service_redirect(request):
#     # tourpackeges = TourPackage.objects.all()
#     user = request.user
#     user_profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
#     my_companies = Company.objects.filter(profile=user_profile)
#     # url = reverse('create_product_service', kwargs={'company_id': my_companies.first().id})
#     # return HttpResponse(url)
#     # if my_companies.count() == 1:
#     #     url = reverse('create_product_service', kwargs={'company_id': my_companies.first().id})
#     #     return HttpResponseRedirect(url)
#     context = {
#         'companies': my_companies,
#     }
#
#
#     return render(request, 'profile/product_or_service/list_product_service_redirect.html', context=context)


@login_required(login_url='sign_in')
def list_product_service(request, company_id):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    user_profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    company = get_object_or_404(Company, id=company_id,
                                profile=user_profile)  # compamy eventler ucun tekrar sorgu getmemesi ucun
    company_product_or_service_list = CompanyProductOrService.objects.filter(deleted=False).filter(company=company)
    # .filter(start_date__gte=now).filter(end_date__lte=now)[:18]
    # contact_list = Contacts.objects.all()
    paginator = FlynsarmyPaginator(company_product_or_service_list, 30, adjacent_pages=3)  # Show 25 contacts per page

    page = request.GET.get('page')  # page check is tam eded
    try:
        company_products_or_services = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        company_products_or_services = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        company_products_or_services = paginator.page(paginator.num_pages)
    context = {
        'company': company,
        # 'ImageFormSet': ImageFormSet,
        'company_products_or_services': company_products_or_services,
    }
    return render(request, 'profile/product_or_service/company_products_or_services.html', context=context)


@login_required(login_url='sign_in')
def create_product_service(request, company_id):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    user_profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'),
                                     user=user)  # compamyler ucun tekrar sorgu getmemesi ucun
    company = get_object_or_404(Company, id=company_id, profile=user_profile)
    next_url = request.GET.get('next_url')

    form = CompanyProductOrServiceForm(request.POST or None, request.FILES or None)
    # ImageFormSet = modelformset_factory(CompanyProductOrServiceImage,
    #                                     form=CompanyProductOrServiceImageForm, extra=3)
    context = {
        'form': form,
        # 'ImageFormSet': ImageFormSet,
        'next_url': next_url,
    }

    if request.method == 'POST':
        if form.is_valid():
            clean_data = form.cleaned_data
            product_or_service = clean_data.get('product_or_service')
            name = clean_data.get('name')
            logo = clean_data.get('logo')
            if not logo:
                form.add_error('logo', _('this_field_is_required'))
                return render(request, 'profile/product_or_service/create_or_edit_product_service.html',
                              context=context)
            slogan = clean_data.get('slogan')
            is_active = clean_data.get('is_active')
            quantity = clean_data.get('quantity')
            price = clean_data.get('price')
            businness_types = clean_data.get('businnes_type')
            businnes_types_parent = clean_data.get('businnes_types_parent')
            currency = clean_data.get('currency')
            description = clean_data.get('description')
            o_product_or_service = get_object_or_404(ProductOrService, id=product_or_service)
            o_currency = get_object_or_404(Currency, id=currency)
            if is_active:
                is_active = True
            else:
                is_active = False
            businness_types_o = Businnes.objects.filter(id__in=businness_types)
            businnes_types_parents_o = Businnes.objects.filter(id__in=businnes_types_parent)
            if businnes_types_parents_o:
                for businnes_types_parent_o in businnes_types_parents_o:
                    if businnes_types_parent_o.parent_id:
                        businness_types_o = businness_types_o.exclude(id=businnes_types_parent_o.parent_id)

            company_product_or_sevice_o = CompanyProductOrService(company=company,
                                                                  product_or_service=o_product_or_service,
                                                                  name=name,
                                                                  logo=logo,
                                                                  slogan=slogan,
                                                                  quantity=quantity,
                                                                  price=price,
                                                                  currency=o_currency,
                                                                  description=description,
                                                                  active=is_active,
                                                                  deleted=False
                                                                  )
            for o_businnes_type in businness_types_o:
                company_product_or_sevice_o.businness_types.add(o_businnes_type)
            for businnes_types_parent_o in businnes_types_parents_o:
                company_product_or_sevice_o.businness_types.add(businnes_types_parent_o)

            company_product_or_sevice_o.save()
            for each in clean_data['images']:  # deyisene menimsedib istifade etmek
                CompanyProductOrServiceImage.objects.create(image=each,
                                                            company_product_or_service=company_product_or_sevice_o)
            next_url = request.GET.get('next_url')
            if not next_url:
                next_url = '/' + request.LANGUAGE_CODE + '/profile/company/product-or-service/add/' + str(
                    company.id) + '/'
            return HttpResponseRedirect(next_url + '?messages=' + 'Succesfuly Added')
            # else:
            # else:
            # postForm = PostForm()
            # formset = ImageFormSet(queryset=CompanyProductOrServiceImage.objects.none())
            # context.update({'formset':formset})
    # context = {
    #     'form':form,
    # }
    return render(request, 'profile/product_or_service/create_or_edit_product_service.html', context=context)


@login_required(login_url='sign_in')
def edit_product_service(request, company_id, cp_id):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    user_profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    company = get_object_or_404(Company, id=company_id, profile=user_profile)
    company_product_service = get_object_or_404(CompanyProductOrService, id=cp_id, company=company)
    next_url = request.GET.get('next_url')
    businnes_type_list = []
    for company_product_businnes_type in company_product_service.businness_types.filter(parent=None):
        businnes_type_list.append(company_product_businnes_type.id)
    businnes_type_parent_list = []
    for company_product_businnes_type in company_product_service.businness_types.exclude(parent=None):
        businnes_type_parent_list.append(company_product_businnes_type.id)
        if not company_product_businnes_type.id in businnes_type_list and company_product_businnes_type.parent_id:
            businnes_type_list.append(company_product_businnes_type.parent_id)
    form = CompanyProductOrServiceForm(request.POST or None, request.FILES or None,
                                       initial={
                                           'product_or_service': company_product_service.product_or_service.id,
                                           'name': company_product_service.name,
                                           'type': company_product_service.type,
                                           'slogan': company_product_service.slogan,
                                           'is_active': company_product_service.active,
                                           'businnes_type': businnes_type_list,
                                           'businnes_types_parent': businnes_type_parent_list,
                                           'quantity': company_product_service.quantity,
                                           'price': company_product_service.price,
                                           'currency': company_product_service.currency.id,
                                           'description': company_product_service.description,
                                       },
                                       )
    context = {
        'form': form,
        'next_url': next_url,
        'company_product_service': company_product_service,
        'company_product_service_parent_businnes_os': company_product_service.businness_types.exclude(parent=None)
    }

    if request.method == 'POST':
        if form.is_valid():
            clean_data = form.cleaned_data
            product_or_service = clean_data.get('product_or_service')
            name = clean_data.get('name')
            type = clean_data.get('type')
            logo = clean_data.get('logo')
            slogan = clean_data.get('slogan')
            is_active = clean_data.get('is_active')
            quantity = clean_data.get('quantity')
            businness_types = clean_data.get('businnes_type')
            businnes_types_parent = clean_data.get('businnes_types_parent')
            price = clean_data.get('price')
            currency = clean_data.get('currency')
            description = clean_data.get('description')
            o_product_or_service = get_object_or_404(ProductOrService, id=product_or_service)
            o_currency = get_object_or_404(Currency, id=currency)
            if is_active:
                is_active = True
            else:
                is_active = False
            businness_types_o = Businnes.objects.filter(id__in=businness_types)
            businnes_types_parents_o = Businnes.objects.filter(id__in=businnes_types_parent)
            if businnes_types_parents_o:
                for businnes_types_parent_o in businnes_types_parents_o:
                    if businnes_types_parent_o.parent_id:
                        businness_types_o = businness_types_o.exclude(id=businnes_types_parent_o.parent_id)
            company_product_service.company = company
            company_product_service.product_or_service = o_product_or_service
            company_product_service.name = name
            company_product_service.type = type
            if logo:
                company_product_service.logo = logo
            company_product_service.slogan = slogan
            company_product_service.quantity = quantity
            company_product_service.price = price
            company_product_service.currency = o_currency
            company_product_service.description = description
            company_product_service.active = is_active
            # company_product_service.deleted = False
            company_product_service.businness_types.clear()
            for o_businnes_type in businness_types_o:
                company_product_service.businness_types.add(o_businnes_type)
            for businnes_types_parent_o in businnes_types_parents_o:
                company_product_service.businness_types.add(businnes_types_parent_o)
            company_product_service.save()
            for each in clean_data['images']:
                CompanyProductOrServiceImage.objects.create(image=each,
                                                            company_product_or_service=company_product_service)
            next_url = request.GET.get('next_url')
            if not next_url:
                next_url = reverse('list_product_service', kwargs={'company_id': company.id})
                # next_url = '/' + request.LANGUAGE_CODE + '/profile/company/product-or-service/add/' + str(company.id) + '/'
            return HttpResponseRedirect(next_url + '?messages=' + 'Succesfuly Added')
            # else:
            #     return HttpResponse('sasas')
    return render(request, 'profile/product_or_service/create_or_edit_product_service.html', context=context)


@login_required(login_url='sign_in')
def create_company(request):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    user_profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    next_url = request.GET.get('next_url')
    form = CompanyCreateForm(user, request.POST or None, request.FILES or None, )
    context = {
        'form': form,
        'next_url': next_url,
    }
    # return HttpResponse('ewewe')
    if request.method == 'POST':
        # return HttpResponse('sass')
        # logo = request.POST.get('logo')
        # return HttpResponse('ewewe')
        if form.is_valid() :
            # return HttpResponse('DSDSJDKS')
            clean_data = form.cleaned_data
            name = clean_data.get('name')
            logo = clean_data.get('logo')
            cover_photo = clean_data.get('cover_photo')
            slogan = clean_data.get('slogan')
            email = clean_data.get('email')
            phones = clean_data.get('phones')
            voen = clean_data.get('voen')
            bank_account = clean_data.get('bank_account')
            region = clean_data.get('region')
            address = clean_data.get('address')
            # is_active = clean_data.get('is_active')
            businnes_type = clean_data.get('businnes_type')
            businnes_types_parent = clean_data.get('businnes_types_parent')
            practices = clean_data.get('practices')
            position = clean_data.get('position')
            longitude = 0
            latitude = 0

            # return HttpResponse(businnes_type)
            i = 1
            for pos in position:
                if i == 1:
                    latitude = Decimal(pos)
                if i == 2:
                    longitude = Decimal(pos)
                i += 1
            # if logo:
            #     pass
            # else:
            #     form.add_error('logo', _('this_field_is_required'))
            #     return render(request, 'profile/create_or_edit_product_service.html', context=context)

            businness_types_o = Businnes.objects.filter(id__in=businnes_type)
            businnes_types_parents_o = Businnes.objects.filter(id__in=businnes_types_parent)
            if businnes_types_parents_o:
                for businnes_types_parent_o in businnes_types_parents_o:
                    if businnes_types_parent_o.parent_id:
                        businness_types_o = businness_types_o.exclude(id=businnes_types_parent_o.parent_id)
            o_region = get_object_or_404(Region, id=region)
            # return HttpResponse('ewdfsddsdsewe')
            company_o = Company(name=name,
                                logo=logo,
                                cover_photo=cover_photo,
                                slogan=slogan,
                                email=email,
                                phones=phones,
                                voen=voen,
                                bank_account=bank_account,
                                region=o_region,
                                address=address,
                                is_active=False,
                                practices=practices,
                                profile=user_profile,
                                position=Geoposition(latitude, longitude),
                                slug=slugify(name),
                                deleted=False
                                )
            for o_businnes_type in businness_types_o:
                company_o.businnes_type.add(o_businnes_type)
            for businnes_types_parent_o in businnes_types_parents_o:
                company_o.businnes_type.add(businnes_types_parent_o)
            company_o.save()

            attachments = clean_data['attachments']
            for each in attachments:
                CompanyAttachment.objects.create(file=each,company=company_o)
            #     return HttpResponse('he')
            # else:
            #     return HttpResponse('yox')
            next_url = request.GET.get('next_url')
            if not next_url:
                next_url = '/' + request.LANGUAGE_CODE + '/profile/companies/'
            return HttpResponseRedirect(next_url + '?messages=' + 'Succesfuly Added')
            # else:
            #     pass
            # if not request.POST.get('logo'):
            #     # pass
            #     form.add_error('logo', _('this_field_is_required'))
            # else:

    return render(request, 'profile/create_or_edit_company.html', context=context)


from decimal import *


@login_required(login_url='sign_in')
def edit_company(request, c_id):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    user_profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    next_url = request.GET.get('next_url')
    company = get_object_or_404(Company, id=c_id, profile=user_profile)  # profile ve profile company ler param
    # return HttpResponse(Geoposition(company.position.latitude,company.position.longitude))
    businnes_type_list = []
    for company_businnes_type in company.businnes_type.filter(parent=None):
        businnes_type_list.append(company_businnes_type.id)
    businnes_type_parent_list = []
    for company_businnes_type in company.businnes_type.exclude(parent=None):
        businnes_type_parent_list.append(company_businnes_type.id)
        if not company_businnes_type.id in businnes_type_list and company_businnes_type.parent_id:
            businnes_type_list.append(company_businnes_type.parent_id)
    try:
        Geoposition(company.position.latitude, company.position.longitude)
        form = CompanyEditForm(request.POST or None, request.FILES or None, initial={
            'name': company.name,
            'slogan': company.slogan,
            'email': company.email,
            'phones': company.phones,
            'voen': company.voen,
            'bank_account': company.bank_account,
            'address': company.address,
            'businnes_type': businnes_type_list,
            'businnes_types_parent': businnes_type_parent_list,
            'region': company.region,
            'position': Geoposition(company.position.latitude, company.position.longitude),
            'practices': company.practices,
        })
    except:
        form = CompanyEditForm(request.POST or None, request.FILES or None, initial={
            'name': company.name,
            'slogan': company.slogan,
            'email': company.email,
            'phones': company.phones,
            'voen': company.voen,
            'bank_account': company.bank_account,
            'address': company.address,
            'businnes_type': businnes_type_list,
            'businnes_types_parent': businnes_type_parent_list,
            'region': company.region,
            'practices': company.practices,
        })
    context = {
        'form': form,
        'next_url': next_url,
        'company': company,
        'company_parent_businnes_os': company.businnes_type.exclude(parent=None)
    }
    # return HttpResponse('ewewe')
    if request.method == 'POST':
        # return HttpResponse('sass')
        # logo = request.POST.get('logo')
        # return HttpResponse('ewewe')
        if form.is_valid():
            # return HttpResponse('DSDSJDKS')
            clean_data = form.cleaned_data
            name = clean_data.get('name')
            logo = clean_data.get('logo')
            cover_photo = clean_data.get('cover_photo')
            slogan = clean_data.get('slogan')
            email = clean_data.get('email')
            phones = clean_data.get('phones')
            voen = clean_data.get('voen')
            bank_account = clean_data.get('bank_account')
            region = clean_data.get('region')
            address = clean_data.get('address')
            businnes_type = clean_data.get('businnes_type')
            businnes_types_parent = clean_data.get('businnes_types_parent')
            practices = clean_data.get('practices')
            position = clean_data.get('position')

            # if logo:
            #     pass
            # else:
            #     form.add_error('logo', _('this_field_is_required'))
            #     return render(request, 'profile/create_or_edit_product_service.html', context=context)

            businness_types_o = Businnes.objects.filter(id__in=businnes_type)
            businnes_types_parents_o = Businnes.objects.filter(id__in=businnes_types_parent)
            if businnes_types_parents_o:
                for businnes_types_parent_o in businnes_types_parents_o:
                    if businnes_types_parent_o.parent_id:
                        businness_types_o = businness_types_o.exclude(id=businnes_types_parent_o.parent_id)
            o_region = get_object_or_404(Region, id=region)
            longitude = 0
            latitude = 0

            # return HttpResponse(businnes_type)
            i = 1
            for pos in position:
                if i == 1:
                    latitude = Decimal(pos)
                if i == 2:
                    longitude = Decimal(pos)
                i += 1
                # return HttpResponse(pos)

            company.name = name
            if logo:
                company.logo = logo
            if cover_photo:
                company.cover_photo = cover_photo
            company.slogan = slogan
            company.email = email
            company.phones = phones
            company.voen = voen
            company.bank_account = bank_account
            company.region = o_region
            company.address = address
            # company.is_active=is_active
            company.practices = practices
            company.position = Geoposition(latitude, longitude)
            # company.position.longitude = longitude
            company.profile = user_profile
            company.slug = slugify(name)
            # company.deleted=False
            company.businnes_type.clear()
            for o_businnes_type in businness_types_o:
                company.businnes_type.add(o_businnes_type)
            for o_businnes_type_parent in businnes_types_parents_o:
                company.businnes_type.add(o_businnes_type_parent)
            company.save()
            attachments = clean_data['attachments']
            if attachments:
                for each in attachments:
                    CompanyAttachment.objects.create(file=each,company=company)
            #     return HttpResponse('he')
            # else:
            #     return HttpResponse('yox')
            next_url = request.GET.get('next_url')
            if not next_url:
                next_url = '/' + request.LANGUAGE_CODE + '/profile/companies/'
            return HttpResponseRedirect(next_url + '?messages=' + 'Succesfuly Added')
            # else:
            #     return HttpResponse('no vlid')
            # if not request.POST.get('logo'):
            #     # pass
            #     form.add_error('logo', _('this_field_is_required'))
            # else:

    return render(request, 'profile/create_or_edit_company.html', context=context)


@login_required(login_url='sign_in')
def my_events(request):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    # tourpackeges = None
    events = Event.objects.filter(company__profile=profile).filter(
        deleted=False)  # profile ve profile company ler param

    context = {
        'profile': profile,
        'events': events,
    }
    return render(request, 'profile/tender/tenders.html', context=context)


@login_required(login_url='sign_in')
def my_event_appeals(request):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    # tourpackeges = None
    events = Event.objects.filter(company__profile=profile).filter(
        deleted=False)  # profile ve profile company ler param

    context = {
        'profile': profile,
        'events': events,
    }
    return render(request, 'profile/tender/tenders.html', context=context)


@login_required(login_url='sign_in')
def company_request_event_appeal_redirect(request):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    user_profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    my_companies = Company.objects.filter(profile=user_profile).filter(is_active=True,
                                                                       deleted=False)  # profile ve profile company ler param
    context = {
        # 'action_slug': action_slug,
        'companies': my_companies,
    }

    return render(request, 'profile/tender/company_event_appeal_redirect.html', context=context)


@login_required(login_url='sign_in')
def my_company_request_events(request, c_id):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    company = get_object_or_404(Company, id=c_id)
    event_appeals = EventAppeal.objects.filter(company=company)  # profile ve profile company ler param
    event_appeal_list = []
    for event_appeal in event_appeals:
        event_appeal_list.append(event_appeal.id)
    events = Event.objects.filter(id__in=event_appeal_list).filter(deleted=False)

    context = {
        'profile': profile,
        'company': company,
        'events': events,
    }
    return render(request, 'profile/tender/my_appeal_events.html', context=context)


@login_required(login_url='sign_in')
def my_company_events(request, c_id):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    company = get_object_or_404(Company, id=c_id)
    events = Event.objects.filter(company=company).filter(deleted=False)  # profile ve profile company ler param

    context = {
        'profile': profile,
        'company': company,
        'events': events,
    }
    return render(request, 'profile/tender/tenders.html', context=context)


@login_required(login_url='sign_in')
def my_company_event_appeals(request, c_id, e_id):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    company = get_object_or_404(Company, profile=profile, id=c_id)
    event = get_object_or_404(Event, company=company, id=e_id, deleted=False)
    event_appeals = EventAppeal.objects.filter(event=event)  # profile ve profile company ler param
    event_appeal_result = EventAppealResult.objects.filter(event=event).first()
    context = {
        'profile': profile,
        'company': company,
        'event': event,
        'event_appeals': event_appeals,
        'event_appeal_result': event_appeal_result,
    }
    return render(request, 'profile/tender/tender_appeals.html', context=context)


@login_required(login_url='sign_in')
def my_company_event_appeal_confirm(request, c_id, e_id, ae_id):
    now = timezone.now()
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    # return HttpResponse('dsdkjsk')
    profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    # return HttpResponse('profile')
    company = get_object_or_404(Company, profile=profile, id=c_id)
    # return HttpResponse('company')
    event = get_object_or_404(Event, company=company, id=e_id, deleted=False)
    # return HttpResponse('event')
    event_appeal = get_object_or_404(EventAppeal, event=event, id=ae_id)
    # return HttpResponse('eventappeal')
    message_code = 0
    message = ''
    data = {}
    if request.method == 'GET' and request.is_ajax():
        if event.end_date < now and event.start_date < now:
            appeal_result = EventAppealResult.objects.filter(event=event)
            from_email = settings.EMAIL_HOST_USER
            to = event_appeal.company.email
            if appeal_result:
                success_title = _('cancled_appeal_title')
                success_content = _('cancled_appeal_content')
                notification_o = Notification(profile=event_appeal.company.profile, event=event, title=success_title,
                                              content=success_content)
                notification_o.save()
                # text_content = 'This is an important message.'
                # html_content = '<p>This is an <strong>important</strong> message.</p>'
                event_url = 'http://127.0.0.1:7000/' + reverse('event', kwargs={'e_id': event_appeal.event_id})
                html_content = '<a href="' + event_url + '" >' + '<p>' + '<img width="100"  src="' + 'http://kiaofportland.com/wp-content/plugins/designhouse5-kia-offers/assets/img/special_offer_tag.png' + '"><span>' + event_appeal.event.name + '</span>' + '</p></a><p>' + success_content + '</p>'
                msg = EmailMultiAlternatives(success_title, success_content, from_email, to)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                appeal_result.delete()
                # appeal_result.eventappeal = event_appeal
                # appeal_result.is_ative = False
                # appeal_result.save()
                message = _('succesfully_unconfirmed_event_appeal')
                message_code = 2
                data = {'message_code': message_code, 'message': message}
            else:
                appeal_result_o = EventAppealResult(
                    event=event,
                    eventappeal=event_appeal,
                    is_ative=True
                )
                appeal_result_o.save()
                success_title = _('confirmed_appeal_title')
                success_content = _('confirmed_appeal_content')
                notification_o = Notification(profile=event_appeal.company.profile, event=event, title=success_title,
                                              content=success_content)
                notification_o.save()
                message = _('succesfully_confirmed_event_appeal')
                message_code = 1
                data = {'message_code': message_code, 'message': message}
                event_url = 'http://127.0.0.1:7000/' + reverse('event', kwargs={'e_id': event_appeal.event_id})
                html_content = '<a href="' + event_url + '" >' + '<p>' + '<img width="100"  src="' + 'http://kiaofportland.com/wp-content/plugins/designhouse5-kia-offers/assets/img/special_offer_tag.png' + '"><span>' + event_appeal.event.name + '</span>' + '</p></a><p>' + success_content + '</p>'
                msg = EmailMultiAlternatives(success_title, success_content, from_email, to)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
        elif event.end_date > now:
            message = _('end_date_greater_than_now_date_message')
            message_code = 0
            data = {'message_code': message_code, 'message': message}
        elif event.start_date > now:
            message = _('start_date_greater_than_now_date_message')
            message_code = 0
            data = {'message_code': message_code, 'message': message}
        # data = {'message_code': message_code, 'message': message}
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")
    else:
        raise Http404


@login_required(login_url='sign_in')
def event_create(request, c_id):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    company = get_object_or_404(Company, id=c_id, profile=profile)  # profile ve profile company ler param
    next_url = request.GET.get('next_url')
    form = EventCreateForm(company.id, request.POST or None, request.FILES or None)
    context = {
        'form': form,
        'next_url': next_url,
    }
    if request.method == 'POST':
        if form.is_valid():
            clean_data = form.cleaned_data
            name = clean_data.get('name')
            company_product_or_service = clean_data.get('company_product_or_service')
            image = clean_data.get('image')
            quantity = clean_data.get('quantity')
            businness_types = clean_data.get('businnes_type')
            businnes_types_parent = clean_data.get('businnes_types_parent')
            price = clean_data.get('price')
            currency = clean_data.get('currency')
            description = clean_data.get('description')
            is_active = clean_data.get('is_active')
            start_date = clean_data.get('start_date')
            end_date = clean_data.get('end_date')
            position = clean_data.get('position')
            longitude = 0
            latitude = 0

            # return HttpResponse(businnes_type)
            i = 1
            for pos in position:
                if i == 1:
                    latitude = Decimal(pos)
                if i == 2:
                    longitude = Decimal(pos)
                i += 1
            businness_types_o = Businnes.objects.filter(id__in=businness_types)
            businnes_types_parents_o = Businnes.objects.filter(id__in=businnes_types_parent)
            if businnes_types_parents_o:
                for businnes_types_parent_o in businnes_types_parents_o:
                    if businnes_types_parent_o.parent_id:
                        businness_types_o = businness_types_o.exclude(id=businnes_types_parent_o.parent_id)
            o_company_product_or_service = get_object_or_404(CompanyProductOrService, id=company_product_or_service,
                                                             company=company)
            o_currency = get_object_or_404(Currency, id=str(currency))

            if is_active:
                is_active = True
            else:
                is_active = False
            # return HttpResponse('ewdfsddsdsewe')

            event_o = Event(name=name,
                            company=company,
                            company_product_or_service=o_company_product_or_service,
                            image=image,
                            quantity=quantity,
                            price=price,
                            currency=o_currency,
                            description=description,
                            is_active=is_active,
                            start_date=start_date,
                            end_date=end_date,
                            position=Geoposition(latitude, longitude),
                            deleted=False
                            )
            # return HttpResponse(businness_types_o.count())

            # for o_businnes_type in businness_types_o:
            #     event_o.businness_types.add(o_businnes_type)
            # print(event_o.businness_types)
            event_o.save()
            for o_businnes_type in businness_types_o:
                event_o.businness_types.add(o_businnes_type)
            for businnes_types_parent_o in businnes_types_parents_o:
                event_o.businness_types.add(businnes_types_parent_o)
            # print(event_o.businness_types)
            event_o.save()

            email_to_list = []
            utl_company_bool = False
            utl_profile_bool = False
            utl_companies = Company.objects.filter(is_active=True, deleted=False)
            for utl_company in utl_companies:
                for utl_company_businnes_type in utl_company.businnes_type.all():
                    if utl_company_businnes_type in businness_types_o:
                        utl_company_bool = True
                        break
                if utl_company_bool:
                    email_to_list.append(utl_company.email)
                utl_company_bool = False
            utl_profiles = Profile.objects.exclude(type='ordinary_person').exclude(type='admin-person')
            for utl_profile in utl_profiles:
                for utl_profile_businnes_type in utl_profile.businnes_type.all():
                    if utl_profile_businnes_type in businness_types_o:
                        utl_profile_bool = True
                        break
                if utl_profile_bool:
                    email_to_list.append(utl_profile.user.email)
                utl_profile_bool = False
            subject, from_email, to = _('add_new_event'), settings.EMAIL_HOST_USER, email_to_list
            # return HttpResponse(email_to_list)
            # try:
            # mail = send_mail(
            #     subject,
            #     'Here is the message.',
            #     settings.EMAIL_HOST_USER,
            #     email_to_list,
            #     fail_silently=False,
            # )
            # mail.se
            text_content = 'This is an important message.'
            # html_content = '<p>This is an <strong>important</strong> message.</p>'
            event_url = 'http://127.0.0.1:7000/' + reverse('event', kwargs={'e_id': event_o.id})
            html_content = '<a href="' + event_url + '" >' + '<p>' + '<img width="100"  src="' + 'http://kiaofportland.com/wp-content/plugins/designhouse5-kia-offers/assets/img/special_offer_tag.png' + '"><span>' + event_o.name + '</span>' + '</p></a>'
            try:
                msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except:
                pass
            #     return HttpResponse('he')
            # else:
            #     return HttpResponse('yox')
            next_url = request.GET.get('next_url')
            if not next_url:
                next_url = '/' + request.LANGUAGE_CODE + '/profile/my-events/company/' + str(company.id) + '/'
            return HttpResponseRedirect(next_url + '?messages=' + 'Succesfuly Added')

            # else:
            #     pass
            # if not request.POST.get('logo'):
            #     # pass
            #     form.add_error('logo', _('this_field_is_required'))
            # else:
    return render(request, 'profile/tender/tender_create_or_edit.html', context=context)


@login_required(login_url='sign_in')
def event_edit(request, c_id, e_id):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    company = get_object_or_404(Company, id=c_id, profile=profile)
    next_url = request.GET.get('next_url')
    event = get_object_or_404(Event, id=e_id, deleted=False)  # profile ve profile company ler param
    # event_appeals = EventAppeal.objects.filter(event=event)
    # if event_appeals:
    #     raise Http404
    businnes_type_list = []
    for event_businnes_type in event.businness_types.filter(parent=None):
        businnes_type_list.append(event_businnes_type.id)
    businnes_type_parent_list = []
    for event_businnes_parent_type in event.businness_types.exclude(parent=None):
        businnes_type_parent_list.append(event_businnes_parent_type.id)
        if not event_businnes_parent_type.id in businnes_type_list and event_businnes_parent_type.parent_id:
            businnes_type_list.append(event_businnes_parent_type.parent_id)

    try:
        form = EventEditForm(company.id, request.POST or None, request.FILES or None,
                             initial={
                                 'name': event.name,
                                 'company_product_or_service': event.company_product_or_service_id,
                                 'position': Geoposition(event.position.latitude, event.position.longitude),
                                 'quantity': event.quantity,
                                 # 'price': event.price,
                                 'currency': event.currency.id,
                                 'businnes_type': businnes_type_list,
                                 'businnes_types_parent': businnes_type_parent_list,
                                 'description': event.description,
                                 'is_active': event.is_active,
                                 'start_date': event.start_date,
                                 'end_date': event.end_date,
                             }, )
    except:
        form = EventEditForm(company.id, request.POST or None, request.FILES or None,
                             initial={
                                 'name': event.name,
                                 'company_product_or_service': event.company_product_or_service_id,
                                 'quantity': event.quantity,
                                 # 'price': event.price,
                                 'currency': event.currency.id,
                                 'businnes_type': businnes_type_list,
                                 'description': event.description,
                                 'is_active': event.is_active,
                                 'start_date': event.start_date,
                                 'end_date': event.end_date,
                             }, )
    context = {
        'form': form,
        'next_url': next_url,
        'event': event,
        'event_parent_businnes_os': event.businness_types.exclude(parent=None),
    }
    if request.method == 'POST':
        # return HttpResponse('sass')
        # logo = request.POST.get('logo')
        # return HttpResponse('ewewe')
        if form.is_valid():
            # return HttpResponse('DSDSJDKS')
            clean_data = form.cleaned_data
            name = clean_data.get('name')
            company_product_or_service = clean_data.get('company_product_or_service')
            image = clean_data.get('image')
            quantity = clean_data.get('quantity')
            price = clean_data.get('price')
            currency = clean_data.get('currency')
            description = clean_data.get('description')
            is_active = clean_data.get('is_active')
            start_date = clean_data.get('start_date')
            end_date = clean_data.get('end_date')
            businness_types = clean_data.get('businnes_type')
            businnes_types_parent = clean_data.get('businnes_types_parent')
            position = clean_data.get('position')
            o_company_product_or_service = get_object_or_404(CompanyProductOrService, id=company_product_or_service,
                                                             company=company)
            o_currency = get_object_or_404(Currency, id=str(currency))
            # return HttpResponse(businness_types)
            businness_types_o = Businnes.objects.filter(id__in=businness_types)
            businnes_types_parents_o = Businnes.objects.filter(id__in=businnes_types_parent)
            if businnes_types_parents_o:
                for businnes_types_parent_o in businnes_types_parents_o:
                    if businnes_types_parent_o.parent_id:
                        businness_types_o = businness_types_o.exclude(id=businnes_types_parent_o.parent_id)
            if is_active:
                is_active = True
            else:
                is_active = False
            # return HttpResponse('ewdfsddsdsewe')

            longitude = 0
            latitude = 0

            # return HttpResponse(businnes_type)
            i = 1
            for pos in position:
                if i == 1:
                    latitude = Decimal(pos)
                if i == 2:
                    longitude = Decimal(pos)
                i += 1

            event.name = name
            event.company = company
            event.company_product_or_service = o_company_product_or_service
            if image:
                event.image = image
            event.quantity = quantity
            event.price = price
            event.currency = o_currency
            event.description = description
            event.is_active = is_active
            event.start_date = start_date
            event.end_date = end_date
            # event.deleted=False

            company.position = Geoposition(latitude, longitude)
            event.businness_types.clear()
            for o_businnes_type in businness_types_o:
                event.businness_types.add(o_businnes_type)
            for businnes_types_parent_o in businnes_types_parents_o:
                event.businness_types.add(businnes_types_parent_o)
            event.save()
            #     return HttpResponse('he')
            # else:
            # return HttpResponse('yox')
            next_url = request.GET.get('next_url')
            if not next_url:
                next_url = '/' + request.LANGUAGE_CODE + '/profile/my-events/company/' + str(company.id) + '/'
            return HttpResponseRedirect(next_url + '?messages=' + 'Succesfuly Added')

            # else:
            #     pass
            # if not request.POST.get('logo'):
            #     # pass
            #     form.add_error('logo', _('this_field_is_required'))
            # else:
    return render(request, 'profile/tender/tender_create_or_edit.html', context=context)


@login_required(login_url='sign_in')
def event_redirect(request, action_slug):
    # tourpackeges = TourPackage.objects.all()
    user = request.user
    user_profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    my_companies = Company.objects.filter(profile=user_profile).filter(is_active=True,
                                                                       deleted=False)  # profile ve profile company ler param
    if action_slug == 'company':
        pass
    elif action_slug == 'create':
        pass
    else:
        raise Http404
    # url = reverse('create_product_service', kwargs={'company_id': my_companies.first().id})
    # return HttpResponse(url)
    # if my_companies.count() == 1:
    #     url = reverse('create_product_service', kwargs={'company_id': my_companies.first().id})
    #     return HttpResponseRedirect(url)
    context = {
        'action_slug': action_slug,
        'companies': my_companies,
    }

    return render(request, 'profile/tender/tender_redirect.html', context=context)


@login_required(login_url='sign_in')
def change_password(request):
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    next_url = request.GET.get('next_url')
    form = ChangePasswordForm(request.POST or None)
    context = {
        'form': form,
        'next_url': next_url,
    }

    if request.method == 'POST':
        if form.is_valid():
            clean_data = form.cleaned_data
            new_password = clean_data.get('new_password')
            # if not logo:
            #     form.add_error('logo', _('this_field_is_required'))
            #     return render(request, 'profile/create_or_edit_product_service.html', context=context)
            user.set_password(new_password)
            user.save()

            context.update({'message': _('password_changed_successfully')})
            # else:

    return render(request, 'profile/change_profile/change_password.html', context=context)


@login_required(login_url='sign_in')
def change_photo(request):
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    next_url = request.GET.get('next_url')
    form = ChangePhotoForm(request.POST or None, request.FILES or None)
    context = {
        'form': form,
        'next_url': next_url,
        'user_profile': user_profile,
    }

    if request.method == 'POST':
        if form.is_valid():
            clean_data = form.cleaned_data
            image = clean_data.get('image')
            # if not logo:
            #     form.add_error('logo', _('this_field_is_required'))
            #     return render(request, 'profile/create_or_edit_product_service.html', context=context)
            user_profile.image = image
            user_profile.save()
            # if user_profile.save():
            #     return HttpResponse('he')
            # user.save()

            context.update({'message': _('photo_changed_successfully')})
            # else:
            #     return HttpResponse('no valid')

    return render(request, 'profile/change_profile/change_photo.html', context=context)




@login_required(login_url='sign_in')
def change_profile_data(request,e_slug):
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    user_profile_data = ChangeProfileInfo.objects.filter(profile=user_profile).filter(admin_confirm=False,admin_reject=False).order_by('-date')
    e_slug_value = ''
    post_success_tf = False
    post_tf = False
    post_message = ''
    next_url = request.GET.get('next_url')
    if e_slug == 'edit':
        if user_profile_data.count() >= 1:
            used_data = user_profile
            e_slug_value = 'edit'
        else:
            used_data = user_profile_data
            e_slug_value = 'new'
    elif e_slug == 'new':
        used_data = user_profile
        e_slug_value = 'new'
    else:
        raise Http404
    user_profile_data = user_profile_data.first()
    if e_slug_value == 'new':
        # return HttpResponse('new')
        businnes_type_list = []
        for user_profile_businnes_type in user_profile.businnes_type.filter(parent=None):
            businnes_type_list.append(user_profile_businnes_type.id)
        businnes_type_parent_list = []
        for user_profile_businnes_type in user_profile.businnes_type.exclude(parent=None):
            businnes_type_parent_list.append(user_profile_businnes_type.id)
            if not user_profile_businnes_type.id in businnes_type_list and user_profile_businnes_type.parent_id:
                businnes_type_list.append(user_profile_businnes_type.parent_id)
        form = ChangeProfileInfoForm(request.user.id,request.POST or None,
                                           initial={
                                               'first_name': user_profile.user.first_name,
                                               'last_name': user_profile.user.last_name,
                                               'username': user_profile.user.username,
                                               'email': user_profile.user.email,
                                               'type': user_profile.type,
                                               'businnes_types': businnes_type_list,
                                               'businnes_types_parent': businnes_type_parent_list,
                                               'voen': user_profile.voen,
                                               'bank_account': user_profile.bank_account,
                                               'region': user_profile.region.id,
                                               'address': user_profile.address,
                                               'practices': user_profile.practices,
                                           },
                                           )

    elif e_slug_value == 'edit':
        # return HttpResponse('edit')
        businnes_type_list = []
        for user_profile_businnes_type in user_profile_data.businnes_type.filter(parent=None):
            businnes_type_list.append(user_profile_businnes_type.id)
        businnes_type_parent_list = []
        # return HttpResponse('dsdskdj')
        for user_profile_businnes_type in user_profile_data.businnes_type.exclude(parent=None):
            businnes_type_parent_list.append(user_profile_businnes_type.id)
            if not user_profile_businnes_type.id in businnes_type_list and user_profile_businnes_type.parent_id:
                businnes_type_list.append(user_profile_businnes_type.parent_id)
        form = ChangeProfileInfoForm(request.user.id,request.POST or None,
                                           initial={
                                               'first_name': user_profile_data.first_name,
                                               'last_name': user_profile_data.last_name,
                                               'username': user_profile_data.username,
                                               'email': user_profile_data.email,
                                               'type': user_profile_data.type,
                                               'businnes_types': businnes_type_list,
                                               'businnes_types_parent': businnes_type_parent_list,
                                               'voen': user_profile_data.voen,
                                               'bank_account': user_profile_data.bank_account,
                                               'region': user_profile_data.region.id,
                                               'address': user_profile_data.address,
                                               'practices': user_profile_data.practices,
                                           },
                                           )
    else:
        raise Http404
    context = {
        'form': form,
        'next_url': next_url,
        'user_profile': user_profile,
    }

    if request.method == 'POST':
        post_tf = True
        if form.is_valid():
            clean_data = form.cleaned_data
            first_name = clean_data.get('first_name')
            last_name = clean_data.get('last_name')
            username = clean_data.get('username')
            email = clean_data.get('email')
            type = clean_data.get('type')
            voen = clean_data.get('voen')
            bank_account = clean_data.get('bank_account')
            region = clean_data.get('region')
            address = clean_data.get('address')
            businnes_types = clean_data.get('businnes_types')
            businnes_types_parent = clean_data.get('businnes_types_parent')
            practices = clean_data.get('practices')
            password = clean_data.get('password')
            region_o = Region.objects.filter(id=region).first()
            if User.objects.filter(username=username).exclude(id=request.user.id):
                form.add_error('username', _('username_allready_use'))
            if User.objects.filter(email=email).exclude(id=request.user.id):
                form.add_error('email', _('email_allready_use'))
            core = authenticate(username=user.username, password=password)
            if not core:
                form.add_error('password', _('your_password_is_incorrect'))
            if user_profile.type != 'admin-person':
                if not type:
                    form.add_error('type', _('type_is_incorrect'))
            if form.errors:
                return render(request, 'profile/change_profile/change_profile_details.html', context=context)
            businness_types_o = Businnes.objects.filter(id__in=businnes_types)
            businnes_types_parents_o = Businnes.objects.filter(id__in=businnes_types_parent)
            if businnes_types_parents_o:
                for businnes_types_parent_o in businnes_types_parents_o:
                    if businnes_types_parent_o.parent_id:
                        businness_types_o = businness_types_o.exclude(id=businnes_types_parent_o.parent_id)
            if user_profile.user.email == email:
                email_confirm = True
            else:
                email_confirm = False
            if user_profile.type == 'admin-person' or user_profile.type == 'ordinary-person' and type == 'ordinary-person':
                # return HttpResponse('Salam')
                user_profile.user.first_name = first_name
                user_profile.user.last_name = last_name
                user_profile.user.username = username
                user_profile.user.email = email
                user_profile.region = region_o
                user_profile.businnes_type.clear()
                for o_businnes_type in businness_types_o:
                    user_profile.businnes_type.add(o_businnes_type)
                for o_businnes_type_parent in businnes_types_parents_o:
                    user_profile.businnes_type.add(o_businnes_type_parent)
                user_profile.user.save()
                user_profile.save()
                post_success_tf = True
                post_message = _('succesfully_changed_profile_data')
                context.update({
                    'message': post_message,
                    'post_success_tf': post_success_tf,
                    'post_message': post_message,
                })
            else:


                if e_slug_value == 'edit' and user_profile_data:
                    if first_name != user_profile_data.first_name or last_name != user_profile_data.last_name or user_profile_data.type != type or user_profile_data.voen != voen or user_profile_data.bank_account != bank_account or user_profile_data.region != region_o or user_profile_data.address != address or user_profile_data.practices != practices:
                        user_profile_data.first_name = first_name
                        user_profile_data.last_name = last_name
                        user_profile_data.type = type
                        user_profile_data.voen = voen
                        user_profile_data.bank_account = bank_account
                        user_profile_data.region = region_o
                        user_profile_data.address = address
                        user_profile_data.practices = practices
                        user_profile_data.admin_confirm = False
                        user_profile_data.admin_reject = False
                        user_profile_data.save()
                    user_profile.user.username = username
                    user_profile.user.email = email
                    user_profile.user.save()
                elif e_slug_value == 'new':
                    if first_name != user_profile.user.first_name or last_name != user_profile.user.last_name or user_profile.type != type or user_profile.voen != voen or user_profile.bank_account != bank_account or user_profile.region != region_o or user_profile.address != address or user_profile.practices != practices:
                        if type == 'ordinary-person':
                            user_profile_data = ChangeProfileInfo(
                                profile=user_profile,
                                first_name=first_name,
                                last_name=last_name,
                                username=username,
                                email=email,
                                type=type,
                                # voen=voen,
                                # bank_account=bank_account,
                                region=region_o,
                                # address=address,
                                # practices=practices,
                                admin_reject=False,
                                admin_confirm=False,
                                email_confirm=email_confirm,
                            )
                        else:
                            user_profile_data = ChangeProfileInfo(
                                profile=user_profile,
                                first_name=first_name,
                                last_name=last_name,
                                username=username,
                                email=email,
                                type=type,
                                voen=voen,
                                bank_account=bank_account,
                                region=region_o,
                                address=address,
                                practices=practices,
                                admin_reject=False,
                                admin_confirm=False,
                                email_confirm=email_confirm
                            )
                        user_profile_data.save()
                    user_profile.user.username = username
                    user_profile.user.email = email
                    user_profile.user.save()

                    # user_profile.businnes_type.clear()
                    for o_businnes_type in businness_types_o:
                        user_profile_data.businnes_type.add(o_businnes_type)
                    for o_businnes_type_parent in businnes_types_parents_o:
                        user_profile_data.businnes_type.add(o_businnes_type_parent)
                    user_profile_data.save()
                else:
                    pass
                user_profile.user.username = username
                user_profile.user.email = email
                user_profile.user.save()
                post_message = _('username_and_email_changed.other_changes_wainting')
                post_success_tf = True
                context.update({
                    # 'message': post_message,
                    'post_success_tf': post_success_tf,
                    'post_message': post_message,
                })
            # else:
            #     return HttpResponse('no valid')

    return render(request, 'profile/change_profile/change_profile_details.html', context=context)


import json


@login_required(login_url='sign_in')
def pr_create_product_or_service(request):
    user = request.user
    message_code = 0
    message = ''
    if request.method == 'GET' and request.is_ajax():
        name = strip_tags(request.GET.get('product_or_service_name'))
        if len(str(name)) < 2:
            message = _('name_greater_than_1_character')
            data = {'message_code': message_code, 'message': message}
        else:
            product_or_service_o = ProductOrService.objects.filter(name=str(name).lower())
            if product_or_service_o:
                message = _('allready_product')
                data = {'message_code': message_code, 'message': message}
            else:
                product_or_service = ProductOrService(name=str(name).lower(), slug=slugify(name))
                product_or_service.save()
                message_code = 1
                message = _('saved_succesfully')
                data = {'message_code': message_code, 'message': message, 'po_id': str(product_or_service.id),
                        'po_label': product_or_service.name}

        # data = {'message_code': message_code, 'message': message}
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")


@login_required(login_url='sign_in')
def notifications(request):
    user = request.user
    profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), user=user)
    notification_list = Notification.objects.filter(profile=profile).order_by('-date')  # bir sorguda goturmek
    paginator = FlynsarmyPaginator(notification_list, 50, adjacent_pages=3)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        notifications = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        notifications = paginator.page(paginator.num_pages)
    context = {
        'notifications': notifications,
    }
    return render(request, 'profile/change_profile/notifications.html', context=context)

@login_required(login_url='sign_in')
def deleted_product_or_service(request, ps_id):
    user = request.user
    profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)

    next_url = request.GET.get('next_url')
    if next_url:
        next_url = strip_tags(next_url)
    else:
        next_url = ''
    cps_o = CompanyProductOrService.objects.filter(company__profile=profile).filter(id=ps_id).first()
    # if cps_o:
    #     return HttpResponse('he')
    # else:
    #     return HttpResponse('yox')
    if cps_o:
        if cps_o.deleted == True:
            cps_o.deleted = False
            # cps_o.active = True
        else:
            cps_o.deleted = True
            # cps_o.active = False
        cps_o.save()
        if next_url:
            pass
            # return HttpResponseRedirect(next_url)
        else:
            next_url = reverse('recycle_bin', kwargs={'content_slug': 'products-or-services'})
        return HttpResponseRedirect(next_url)
    else:
        raise Http404

@login_required(login_url='sign_in')
def deleted_event(request, e_id):
    user = request.user
    profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    next_url = strip_tags(request.GET.get('next_url'))
    element_deleted_message = ''
    e_o = Event.objects.filter(company__profile=profile).filter(id=e_id).first()
    if e_o:
        if e_o.deleted == True:
            e_o.deleted = False
            # e_o.is_active = True
        else:
            e_o.deleted = True
            # e_o.is_active = False
        e_o.save()
        element_deleted_message = _("event_deleted_message")
        if next_url:
            if next_url in '?':
                next_url += '&event-deleted-message=' + element_deleted_message
            else:
                next_url += '?event-deleted-message=' + element_deleted_message
                # return HttpResponseRedirect(next_url)
        else:
            next_url = reverse('my_company_events', kwargs={'c_id': e_o.company.id})
        return HttpResponseRedirect(next_url)

    else:
        raise Http404

@login_required(login_url='sign_in')
def deleted_company(request, c_id):
    user = request.user
    profile = get_object_or_404(Profile, ~Q(type='ordinary-person'), ~Q(type='admin-person'), user=user)
    next_url = strip_tags(request.GET.get('next_url'))
    c_o = Company.objects.filter(profile=profile).filter(id=c_id).first()
    if c_o:
        if c_o.deleted == True:
            c_o.deleted = False
            # c_o.active = True
        else:
            c_o.deleted = True
            # c_o.active = False
        c_o.save()
        if next_url:
            pass
            # return HttpResponseRedirect(next_url)
        else:
            next_url = reverse('my_company_events', kwargs={'c_id': c_o.company.id})
        return HttpResponseRedirect(next_url)
    else:
        raise Http404


def profile_parent_business_ajax(request):
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
        business_ids = request.POST.getlist('businnes_type')
        businnes_types_parent_ids = request.POST.getlist('businnes_types_parent')
        # print('--------------------------')
        # print(businnes_types_parent_ids)
        # print('--------------------------')
        # # for business_id in [business_ids]:
        # #     str+=str(business_id)
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

    data = {'message_code': message_code, 'message': get_parent_business_html_data + get_business_html_data}
    # data = {'message_code': message_code, 'message': message}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")


def profile_parent_business_year_ajax(request):
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
        business_ids = request.POST.getlist('businnes_type_year')
        businnes_types_parent_ids = request.POST.getlist('businnes_types_parent_year')
        # print('--------------------------')
        # print(businnes_types_parent_ids)
        # print('--------------------------')
        # # for business_id in [business_ids]:
        # #     str+=str(business_id)
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
                                # active_option = False
                                # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                                # print(business_parent_os_list)
                                # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                                # print(bp.id)
                                # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                                # bp_id = str(bp.id)
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

    data = {'message_code': message_code, 'message': get_parent_business_html_data + get_business_html_data}
    # data = {'message_code': message_code, 'message': message}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")

@login_required(login_url='sign_in')
def chart_now_year_month_ajax(request):
    message = ''
    html_data = ''
    now = timezone.now()
    message_code = 0
    get_general_html_data = ''
    if request.method == 'POST' and request.is_ajax():
        business_id = request.POST.get('businnes_type_year')
        businnes_types_parent_id = request.POST.get('businnes_types_parent_year')
        year = request.POST.get('year')
        business_o = Businnes.objects.filter(id=business_id).filter(parent=None).first()
        if len(str(businnes_types_parent_id)) > 5:
            business_parent_o = Businnes.objects.filter(id=businnes_types_parent_id).first()
        else:
            business_parent_o = Businnes.objects.filter(active=True).filter(active=False).first()
        # try:
            # if business_parent_o:
            #     main_business = business_parent_o
            # else:
            #     main_business = business_o
        data_list = []
        # print('=======================================')
        if len(str(businnes_types_parent_id)) > 5:
            busines_op_id = businnes_types_parent_id
            # print(busines_op.icon)
        else:
            busines_op_id = business_id
            # print('busines_op.name')
        # print(main_business..name.encode("utf-8"))
        busines_op = Businnes.objects.get(id=busines_op_id)
        # "{:0>4d}".format(year)
        companies_now = Company.objects.filter(deleted=False).filter(date__year=year).filter(businnes_type=busines_op)
        pors_now = CompanyProductOrService.objects.filter(deleted=False).filter(date__year=year).filter(businness_types=busines_op)
        events_now = Event.objects.filter(deleted=False).filter(date__year=year).filter(businness_types=busines_op)
        month_list = [
            {'num': 1, 'name': _('january')},
            {'num': 2, 'name': _('february')},
            {'num': 3, 'name': _('march')},
            {'num': 4, 'name': _('april')},
            {'num': 5, 'name': _('may')},
            {'num': 6, 'name': _('june')},
            {'num': 7, 'name': _('july')},
            {'num': 8, 'name': _('august')},
            {'num': 9, 'name': _('september')},
            {'num': 10, 'name': _('october')},
            {'num': 11, 'name': _('november')},
            {'num': 12, 'name': _('december')},
        ]
        data_list_month = []
        for month_list_item in month_list:
            data_list_month.append(
                {
                    "month_format": "{:0>2d}".format(month_list_item['num']),
                    "month": month_list_item['num'],
                    "month_name": month_list_item['name'],
                    "company_count": companies_now.filter(date__month=month_list_item['num']).count(),
                    "pors_count": pors_now.filter(date__month=month_list_item['num']).count(),
                    "event_count": events_now.filter(date__month=month_list_item['num']).count(),
                }
            )
            get_general_html_data = '{0}{1}'.format(get_general_html_data,
                                                    render_to_string(
                                                        'profile/include/chart/business_all_content_month.html',
                                                        {
                                                            'main_business_name': str(
                                                                busines_op.name),
                                                            'data_list_month': data_list_month,
                                                            'year':year,
                                                            'busines_op':busines_op,
                                                            # 'general_for': general_for,
                                                        }))
        message_code = 1
        # except:
        #     pass
    data = {'message_code': message_code, 'message': get_general_html_data.replace(
        '<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>', '')}
    # data = {'message_code': message_code, 'message': message}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")
@login_required(login_url='sign_in')
def chart_business_ajax(request):
    message = ''
    html_data = ''
    now = timezone.now()
    message_code = 0
    continue_op = False
    get_general_html_data = ''
    get_business_html_data = ''
    string_d = ''
    if request.method == 'POST' and request.is_ajax():
        business_id = request.POST.get('businnes_type')
        businnes_types_parent_id = request.POST.get('businnes_types_parent')
        default_year = 2017
        business_o = Businnes.objects.filter(id=business_id).filter(parent=None).first()
        if len(str(businnes_types_parent_id)) > 5:
            business_parent_o = Businnes.objects.filter(id=businnes_types_parent_id).first()
        else:
            business_parent_o = Businnes.objects.filter(active=True).filter(active=False).first()
        business_year_list = []
        if int(now.year) == default_year:
            business_year_list.append(default_year)
        else:
            if int(now.year) - default_year < 11:
                for x in range(default_year, now.year + 1):
                    business_year_list.append(x)
            else:
                for x in range(int(now.year) - 10, int(now.year + 1)):
                    business_year_list.append(x)
        selected_for = 0
        general_for = 0
        if business_o or business_parent_o:
            try:
                # selected_for = 1
                if business_parent_o:
                    main_business = business_parent_o
                else:
                    main_business = business_o
                data_list = []
                # print('=======================================')
                if len(str(businnes_types_parent_id)) > 5:
                    busines_op_id = businnes_types_parent_id
                    # print(busines_op.icon)
                else:
                    busines_op_id = business_id
                    print('busines_op.name')
                # print(main_business..name.encode("utf-8"))
                busines_op = Businnes.objects.get(id=busines_op_id)
                # print('=======================================')
                # print(busines_op.name.encode("utf-8"))
                # print('=======================================')
                for business_year_list_item in business_year_list:
                    data_list.append(
                        {
                            'year': business_year_list_item,
                            # 'main_business_name': str(busines_op.name.encode("utf-8")),
                            'company_count': Company.objects.filter(businnes_type=main_business).filter(
                                date__year=business_year_list_item).count(),
                            'event_count': Event.objects.filter(businness_types=main_business).filter(
                                date__year=business_year_list_item).count(),
                            'pors_count': CompanyProductOrService.objects.filter(businness_types=main_business).filter(
                                date__year=business_year_list_item).count(),
                        }
                    )

                get_general_html_data = '{0}{1}'.format(get_general_html_data,
                                                        render_to_string(
                                                            'profile/include/chart/business_all_content.html',
                                                            {
                                                                'main_business_name': str(
                                                                    busines_op.name),
                                                                'data_list': data_list,
                                                                # 'general_for': general_for,
                                                            }))

                # data_list_year = []
                # # print('=======================================')
                # # print(business_o.name)
                # # print('=======================================')
                # for business_year_list_item in business_year_list:
                #     data_list_year.append(
                #         {
                #             'year': business_year_list_item,
                #             'main_business': main_business,
                #             'company_count': Company.objects.filter(
                #                 date__year=business_year_list_item).count(),
                #             'event_count': Event.objects.filter(
                #                 date__year=business_year_list_item).count(),
                #             'pors_count': CompanyProductOrService.objects.filter(
                #                 date__year=business_year_list_item).count(),
                #         }
                #     )
                #
                # get_general_html_data = '{0}{1}'.format(get_general_html_data,
                #                                         render_to_string(
                #                                             'profile/include/chart/business_all_content.html',
                #                                             {
                #                                                 # 'parent_tf': True,
                #                                                 'data_list': data_list,
                #                                                 # 'general_for': general_for,
                #                                             }))

                selected_for += 1

                message_code = 2
                html_data = ''
            except:
                message_code = 7
                html_data = ''

    else:
        message_code = 5
        html_data = string_d  # elif not businnes_types_form.is_valid():
        #     html_data = businnes_types_form

    data = {'message_code': message_code, 'message': get_general_html_data.replace(
        '<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>', '')}
    # data = {'message_code': message_code, 'message': message}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")
