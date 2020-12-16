import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from flynsarmy_paginator.paginator import FlynsarmyPaginator
from django.utils.translation import ugettext as _
# Create your views here.
from company.forms import *
from company.models import *
from home.models import *
from general.models import *
from registration.models import *
from payment.models import *
from django.db.models import Q


def companies(request):
    now = timezone.now()
    company_list = Company.objects.filter(deleted=False,is_active=True).exclude(is_active=False,deleted=True)
    events = Event.objects.filter(is_active=True).order_by('-start_date').filter(end_date__gt=now).filter(deleted=False).filter(company__deleted=False,company__is_active=True)[:13]
    company_product_or_services = CompanyProductOrService.objects.filter(active=True).filter(company__deleted=False,company__is_active=True).order_by('?').filter(deleted=False)[:7]
    # contact_list = Contacts.objects.all()
    #paginationa yeniden baxilacaq
    paginator = FlynsarmyPaginator(company_list, 25, adjacent_pages=3) # Show 25 contacts per page

    page = request.GET.get('page') #page check is tam eded
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        companies = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        companies = paginator.page(paginator.num_pages)


    context = {
        'companies':companies,
        'company_product_or_services':company_product_or_services,
        'events':events,
    }
    return render(request, 'company/companies.html', context=context)



def company(request,c_id):
    # now = timezone.now()
    company = get_object_or_404(Company,id=c_id,is_active=True, deleted=False)
    # tourpackeges = None
    events = Event.objects.filter(is_active=True).filter(deleted=False).order_by('-start_date').filter(company=company).filter(company__deleted=False,company__is_active=True)[:10]
    company_products_or_services = CompanyProductOrService.objects.filter(active=True,deleted=False).filter(company=company).filter(company__deleted=False,company__is_active=True)[:10]
    # .filter(start_date__gte=now).filter(end_date__lte=now)[:18]
    context = {
        'company':company,
        'events':events,
        'company_products_or_services':company_products_or_services,
    }
    return render(request, 'company/company.html', context=context)



def company_pagination_content(request,c_id,content_slug,p_number):
    # now = timezone.now()

    if request.method == 'GET' and request.is_ajax():
        company = get_object_or_404(Company,id=c_id,is_active=True, deleted=False)
        # tourpackeges = None
        min_count = (p_number - 1) * 10
        max_count = p_number * 10
        get_general_html_data = ''
        for_datas = 0
        message_code = 0
        if content_slug == 'events':
            datas = Event.objects.filter(is_active=True).filter(deleted=False).order_by('-start_date').filter(company=company).filter(company__deleted=False,company__is_active=True)[min_count:max_count]
            for data in datas:
                for_datas += 1
                get_general_html_data = '{0}{1}'.format(get_general_html_data,
                                                                render_to_string(
                                                                    'include/company/_html_data/_company_events.html',
                                                                    {
                                                                        'data': data,
                                                                        'for_datas': for_datas
                                                                    }))
        elif content_slug == 'company-products-or-services':
            datas = CompanyProductOrService.objects.filter(active=True,deleted=False).filter(company=company).filter(company__deleted=False,company__is_active=True)[min_count:max_count]
            for data in datas:
                for_datas += 1
                get_general_html_data = '{0}{1}'.format(get_general_html_data,
                                                                render_to_string(
                                                                    'include/company/_html_data/_company_pors.html',
                                                                    {
                                                                        'data': data,
                                                                        'for_datas': for_datas
                                                                    }))
        message_code = 1
        data = {'message_code': message_code, 'message': get_general_html_data}
        # data = {'message_code': message_code, 'message': message}
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")
    else:
        raise Http404



def company_product_or_service(request,cp_id):
    # now = timezone.now()
    company_product_or_service = get_object_or_404(CompanyProductOrService, ~Q(company__deleted=True), ~Q(company__is_active=False),id=cp_id,active=True, deleted=False,)
    # tourpackeges = None
    # .filter(start_date__gte=now).filter(end_date__lte=now)[:18]
    context = {
        'company_product_or_service':company_product_or_service,
    }
    return render(request, 'company/product_or_service.html', context=context)




def events(request):
    now = timezone.now()
    rand_events = Event.objects.filter(is_active=True).order_by('?').filter(end_date__gt=now).filter(deleted=False).filter(company__deleted=False,company__is_active=True)[:13]
    rand_company_product_or_services = CompanyProductOrService.objects.filter(active=True).filter(company__deleted=False,company__is_active=True).order_by('?').filter(
        deleted=False)[:7]
    event_list = Event.objects.filter(is_active=True).filter(deleted=False).filter(company__deleted=False,company__is_active=True).order_by('start_date')
    # .filter(start_date__gte=now).filter(end_date__lte=now)[:18]
    # contact_list = Contacts.objects.all()
    paginator = FlynsarmyPaginator(event_list, 30, adjacent_pages=3) # Show 25 contacts per page

    page = request.GET.get('page') #page check is tam eded
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = paginator.page(paginator.num_pages)
    context = {
        'events':events,
        'rand_events':rand_events,
        'rand_company_product_or_services':rand_company_product_or_services,
    }
    return render(request, 'events/events.html', context=context)


def event(request,e_id):
    event = get_object_or_404(Event,is_active=True,id=e_id)
    is_post_val = False
    success_message = ''
    if request.user.is_authenticated():
        user_id = request.user.id # evvelceden teyin edilen tip olub olmafigi check olunmalidi
    else:
        user_id = 0
    context = {
        'event': event,
    }
    try:
        event_longitude = event.position.longitude
        event_latitude = event.position.latitude
    except:
        event_longitude = 49.86709240000005
        event_latitude = 40.40926169999999
        # latitude =
    e_company_id = event.company.id
    event_appeal_form = EventAppealForm(user_id,e_company_id,request.POST or None, request.FILES or None)
    context.update({
        'event_longitude':event_longitude,
        'event_latitude':event_latitude,
        'is_post_val':is_post_val,
        'event_appeal_form':event_appeal_form,
    })
    if request.method == 'POST':
        if not request.user.is_authenticated():
            raise Http404
        user_profile = Profile.objects.filter(user=request.user)
        is_post_val = True
        if event_appeal_form.is_valid():

            clean_data = event_appeal_form.cleaned_data
            company = clean_data.get('company')
            price = clean_data.get('price')
            currency = clean_data.get('currency')
            # return HttpResponse(str(currency))
            currency_o = Currency.objects.filter(id=currency).first()
            company_o = Company.objects.filter(profile=user_profile).filter(id=company).filter(is_active=True,deleted=False).first()
            # if Event.objects.filter(com)
            if company_o:
                event_appeal = EventAppeal.objects.filter(event=event,company=company_o)
                if event_appeal:
                    is_post_val = True
                    event_appeal_form._errors['company'] = 'allready_apply_this_event'
                    context.update({
                        'is_post_val': is_post_val,
                        'event_appeal_form': event_appeal_form,
                        'event_longitude':event_longitude,
                        'event_latitude':event_latitude,
                    })
                    return render(request, 'events/event.html', context=context)
            if not company_o:
                event_appeal_form._errors['company'] = 'please_select_correct_data'
                return render(request, 'events/event.html', context=context)
            event_appeal = EventAppeal(event=event,company=company_o,price=price,currency=currency_o)
            event_appeal.save()
            attachments = clean_data['attachments']
            for each in attachments:
                AttachmentEvent.objects.create(file=each,event_appeal=event_appeal)
            # is_success_val = True
            is_post_val = False
            success_message = _('event_appeal_success_message')

    context.update({
        'success_message':success_message,
        # 'is_post_val':is_post_val,
    })
    return render(request, 'events/event.html', context=context)



from django.core.paginator import EmptyPage, PageNotAnInteger

def busines(request,b_id,bc_slug,):
    now = timezone.now()
    datas = None
    data_list = None
    busines = get_object_or_404(Businnes,id=b_id,active=True)
    rand_events = Event.objects.filter(is_active=True).filter(businness_types=busines).filter(businness_types__parent=busines).filter(end_date__gt=now).filter(deleted=False).filter(company__deleted=False,company__is_active=True).order_by('?')[:13]
    rand_company_product_or_services = CompanyProductOrService.objects.filter(active=True).filter(businness_types=busines).filter(businness_types__parent=busines).filter(
        deleted=False).filter(company__deleted=False,company__is_active=True).order_by('?')[:7]

    if bc_slug == 'events':
        data_list = Event.objects.filter(company__businnes_type=busines).filter(is_active=True).filter(
        deleted=False).filter(company__deleted=False,company__is_active=True).order_by('-start_date')
    elif bc_slug == 'companies':
        data_list = Company.objects.filter(businnes_type__id=busines.id)
        # return HttpResponse(busines.id)
    elif bc_slug == 'products-or-services':
        data_list = CompanyProductOrService.objects.filter(company__businnes_type=busines).filter(company__deleted=False,company__is_active=True)
    else:
        raise Http404

    paginator = FlynsarmyPaginator(data_list, 24, adjacent_pages=3)  # Show 25 contacts per page


    page = request.GET.get('page') #page check is tam eded
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        datas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        datas = paginator.page(paginator.num_pages)
    context = {
        'busines':busines,
        'datas':datas,
        'bc_slug':bc_slug,
        'rand_events': rand_events,
        'rand_company_product_or_services': rand_company_product_or_services,
        # 'company_products_or_services':company_products_or_services,
    }
    return render(request, 'company/business.html', context=context)

def add_cart_ajax(request,ps_id):
    now = timezone.now()
    message_code = 0
    message= ''
    data = {'message_code': message_code, 'message': message}
    if request.method == 'GET' and request.is_ajax():
        if request.user.is_authenticated():
            try:
                pos = CompanyProductOrService.objects.filter(id=ps_id).first()
                add_cart_o = AddCart.objects.filter(user=request.user,company_product_or_service=pos)
                if add_cart_o:
                    add_cart_o.delete()
                    message_code = 2
                else:
                    add_cart_o = AddCart(user=request.user,company_product_or_service=pos,count=1,active=True)
                    add_cart_o.save()
                    message_code = 1
            except:
                pass
        else:
            # try:
            pos = CompanyProductOrService.objects.filter(id=ps_id).first()
            add_list_product_or_services = request.session['add_list_product_or_services']
            if not str(pos.id) in add_list_product_or_services:
                request.session['add_list_product_or_services'] += str(pos.id)
                message_code = 1
            else:
                request.session['add_list_product_or_services'] = str(add_list_product_or_services).replace(str(pos.id), "")
                message_code = 2
            # except:
            #     pass
        data = {
            'message_code': message_code,
            'message': message,
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")
    else:
        raise Http404