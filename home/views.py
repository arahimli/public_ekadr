import json
from django.utils.html import strip_tags

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
# from django.utils import timezone
from home.forms import HomeSearchForm
from registration.models import *
from home.models import *
# from payment.models import *
from company.models import *

from flynsarmy_paginator.paginator import FlynsarmyPaginator
import xmltodict as xmltodict
import urllib.request
import urllib.parse

# from userprofile.models import *
# Create your views here.


def context_processor(request):
    now = timezone.now()
    yesterday = timezone.now() - timezone.timedelta(days=1)
    based_busineses = Businnes.objects.filter(active=True).filter(parent=None).order_by('order_index')
    base_company_info = CompanyInfo.objects.filter(active=True).order_by('-date').first()
    base_useful_links = UsefulLink.objects.filter(active=True).order_by('-order_index')
    based_random_events = Event.objects.filter(is_active=True,deleted=False).filter(company__deleted=False, company__is_active=True).order_by('?')[:12]
    based_random_company_products = CompanyProductOrService.objects.filter().filter(active=True).filter(deleted=False).filter(
        company__deleted=False, company__is_active=True).order_by('?')[:12]
    most_recent_view_company_product_or_services = CompanyProductOrService.objects.filter(active=True,deleted=False).filter(company__deleted=False,company__is_active=True)[:3]
    base_social = Social.objects.filter(active=True).order_by('order_index')
    based_ads = Ads.objects.filter(active=True).order_by('-date').first()
    context = {}
    if request.user.is_authenticated():
        add_cart_carts = AddCart.objects.filter(user=request.user)
        add_cart_carts_list = []
        for add_cart_cart in add_cart_carts:
            add_cart_carts_list.append(add_cart_cart.company_product_or_service_id)
            # print(add_cart_carts_list.)
            context.update({
                    'add_cart_carts':add_cart_carts,
                    'add_cart_carts_list':add_cart_carts_list,
        })
    else:
        try:
            list_product_or_services_session = request.session['add_list_product_or_services']
        except:
            list_product_or_services_session = ''
        context.update({
                'list_product_or_services_session':list_product_or_services_session,
                # 'add_cart_carts_list':add_cart_carts_list,
        })
    currencies_today = CurrencyDaily.objects.filter(date=now.date())
    # # currencies_yesterday = CurrencyDaily.objects.filter(date=yesterday)
    try:
        if not currencies_today.count() == 45:
            currencies = CurrencyDaily.objects.all()
            currencies.delete()
            url_str = 'http://cbar.az/currencies/' + '{0:0=2d}'.format(now.day) + '.' + '{0:0=2d}'.format(
                now.month) + '.' + str(now.year) + '.xml'
            url_str_yesterday = 'http://cbar.az/currencies/' + '{0:0=2d}'.format(yesterday.day) + '.' + '{0:0=2d}'.format(
                yesterday.month) + '.' + str(yesterday.year) + '.xml'
            # # return HttpResponse(url_str_yesterday)
            file = urllib.request.urlopen(url_str)
            data = file.read()
            file.close()
            data = xmltodict.parse(data)
            bank_metals = data['ValCurs']['ValType'][-1]['Valute']
            #******************************************************************
            #******************************************************************
            file_yesterday = urllib.request.urlopen(url_str_yesterday)
            data_yesterday = file_yesterday.read()
            file_yesterday.close()
            data_yesterday = xmltodict.parse(data_yesterday)
            bank_metals_yesterday = data_yesterday['ValCurs']['ValType'][-1]['Valute']
            # ******************************************************************
            # # ******************************************************************

            dic = {}
            i = 4
            j = 0
            for bank_metal in bank_metals:
                # return HttpResponse(bank_metal)

                increase = 0
                for bank_metal_yesterday in bank_metals_yesterday:
                    if bank_metal['@Code'] == bank_metal_yesterday['@Code']:
                        increase = bank_metal_yesterday['Value']
                i+=1
                # if increase > 0:
                #     inc = 'inc'
                # elif increase < 0:
                #     inc = 'dec'
                # else:
                #     inc = 'noc'
                # order_index = 0
                if bank_metal['@Code'] =='USD' :
                    order_index = 1
                elif bank_metal['@Code'] == 'EUR':
                    order_index = 2
                elif bank_metal['@Code'] == 'RUB':
                    order_index = 3
                elif bank_metal['@Code'] == 'TRY':
                    order_index = 4
                else:
                    order_index = i
                # inc = float(bank_metal['Value']) - float(bank_metals_yesterday[0]['Value'])
                # if float(bank_metal['Value']) > float(bank_metals_yesterday[0]['Value']):
                #     inc = 'inc'
                # elif float(bank_metal['Value']) < float(bank_metals_yesterday[0]['Value']):
                #     inc = 'dec'
                # else:
                #     inc = 'noc'
                currency_today_save = CurrencyDaily(currency=bank_metal['Name'],
                                         code=bank_metal['@Code'],
                                         rate=bank_metal['Value'],
                                         difference=increase,
                                         order_index=order_index,
                                         date=now)
                currency_today_save.save()
    except:
        pass
    #
    currencies_today = CurrencyDaily.objects.filter(date=now).order_by('order_index')[:4]
    context.update({
        'now':now,
        'base_company_info':base_company_info,
        'base_useful_links':base_useful_links,
        'most_recent_view_company_product_or_services':most_recent_view_company_product_or_services,
        'base_social':base_social,
        'based_busineses':based_busineses,
        'based_random_events':based_random_events,
        'based_random_company_products':based_random_company_products,
        'currencies_today':currencies_today,
        'based_ads':based_ads,
    })
    if request.user.is_authenticated():
        try:
            user_profile_base = Profile.objects.get(user=request.user)
        except:
            user_profile_base = None
        context.update({'user_profile_base': user_profile_base})
    return context


def index(request):
    now = timezone.now()
    map_companies = Company.objects.filter(deleted=False,is_active=True).exclude(position='')
    map_events = Event.objects.filter(deleted=False,is_active=True).order_by('-start_date').exclude(position='')
    businneses = Businnes.objects.filter(active=True).order_by('order_index')
    home_search_form = HomeSearchForm(request.GET or None)
    first_busines = Businnes.objects.filter(active=True).order_by('order_index').filter(parent=None).first()
    first_events = Event.objects.filter(company__businnes_type=first_busines).filter(is_active=True,deleted=False).filter(company__deleted=False,company__is_active=True)[:6]
    first_company_products = CompanyProductOrService.objects.filter(company__businnes_type=first_busines).filter(active=True).filter(deleted=False).filter(company__deleted=False,company__is_active=True)[:6]
    best_seller_company_products = CompanyProductOrService.objects.filter().filter(active=True).filter(deleted=False).filter(company__deleted=False,company__is_active=True)[:12]
    most_view_company_products = CompanyProductOrService.objects.filter().filter(active=True).filter(deleted=False).filter(company__deleted=False,company__is_active=True)[:12]
    random_company_products = CompanyProductOrService.objects.filter().filter(active=True).filter(deleted=False).filter(company__deleted=False,company__is_active=True).order_by('?')[:12]
    sponsored_events = Event.objects.filter(end_date__lte=now).filter(is_active=True,deleted=False).filter(company__deleted=False,company__is_active=True)[:18]
    sponsored_company_products = CompanyProductOrService.objects.filter(active=True,deleted=False).filter(company__deleted=False,company__is_active=True)[:15]
    events = Event.objects.filter().filter(is_active=True,deleted=False).order_by('start_date').filter(company__deleted=False,company__is_active=True)[:15]
    spec_events = Event.objects.filter().filter(is_active=True,deleted=False).order_by('start_date').filter(company__deleted=False,company__is_active=True)[:15]
    most_popular_events = Event.objects.filter(end_date__lt=timezone.now()).filter(is_active=True,deleted=False).filter(company__deleted=False,company__is_active=True)[:13]
    # return HttpResponse(businneses.count())
    based_partners = Partner.objects.filter(active=True).order_by('order_index')
    based_services = Service.objects.filter(active=True).order_by('order_index')
    context = {
        'businneses':businneses,
        'home_search_form':home_search_form,
        'sponsored_events':sponsored_events,
        'sponsored_company_products_or_services':sponsored_company_products,
        'events':events,
        'spec_events':spec_events,
        'most_popular_events':most_popular_events,
        'first_busines_o':first_busines,
        'first_events':first_events,
        'first_company_products':first_company_products,
        'best_seller_company_products':best_seller_company_products,
        'most_view_company_products':most_view_company_products,
        'map_events':map_events,
        'map_companies':map_companies,
        'random_company_products':random_company_products,
        'based_partners':based_partners,
        'based_services':based_services,
    }
    # return render(request, 'home/index.html', context=context)
    return render(request, 'home/index2.html', context=context)


def faq(request):
    faqs = Faq.objects.filter(active=True).order_by('order_index')
    context = {
        'faqs':faqs,
        # 'sponsored_events':sponsored_events,
        # 'sponsored_company_products_or_services':sponsored_company_products,
    }
    # return render(request, 'home/index.html', context=context)
    return render(request, 'home/faq.html', context=context)




def search(request,sc_slug):
    now = timezone.now()
    search_word = request.GET.get('search')
    businnes_g = request.GET.get('businnes')
    regions_g = request.GET.get('regions')
    if search_word:
        search_word = strip_tags(search_word)
    if businnes_g:
        businnes_g = strip_tags(businnes_g)
    if regions_g:
        regions_g = strip_tags(regions_g)
        if regions_g:
            try:
                int(regions_g)
                # return True
            except:
                raise Http404
    rand_events = Event.objects.filter(is_active=True).order_by('?').filter(end_date__gt=now).filter(deleted=False).filter(company__deleted=False,company__is_active=True)[:13]
    rand_company_product_or_services = CompanyProductOrService.objects.filter(active=True).order_by('?').filter(
        deleted=False).filter(company__deleted=False,company__is_active=True)[:7]
    search_content = sc_slug
    datas = None
    # data_list = None

    if search_content == 'events':
        data_list = Event.objects.filter().filter(deleted=False,is_active=True).filter(company__deleted=False,company__is_active=True)
        if search_word and search_word.strip() != '':
            if data_list:

                data_list = data_list.filter(Q(name__icontains=search_word) | Q(company__name__icontains=search_word) |
                                                      Q(company_product_or_service__name__icontains=search_word)
                                                      | Q(company_product_or_service__product_or_service__name__icontains=search_word)
                                                      ).filter(is_active=True).filter(deleted=False)
        if businnes_g and businnes_g.strip() != '':
            # data_list = Com.objects.filter()
            if data_list:
                data_list = data_list.filter(Q(businness_types__id=businnes_g) | Q(company__businnes_type__id=businnes_g)
                                                  )
        if regions_g and str(regions_g).strip() != '':
            if data_list:
                data_list = data_list.filter(company__region=regions_g)
        else:
            data_list.filter(id=0)


    elif search_content == 'companies':
        data_list = Company.objects.filter().filter(is_active=True).filter(deleted=False)
        if search_word and search_word != '':
            if data_list:
                data_list = data_list.filter(Q(name__icontains=search_word) | Q(slogan__icontains=search_word) |
                                             Q(email__icontains=search_word) | Q(profile__user__first_name__icontains=search_word)
                                               | Q(profile__user__last_name__icontains=search_word)
                                             )
        if businnes_g:
            if data_list:
                data_list = data_list.filter(Q(businnes_type__id=businnes_g))
        if regions_g:
            if data_list:
                data_list = data_list.filter(company__region=regions_g)
        else:
            data_list.filter(id=0)
    elif search_content == 'products-or-services':
        data_list = CompanyProductOrService.objects.filter(active=True).filter(deleted=False).filter(company__deleted=False,company__is_active=True)
        if search_word and search_word != '':
            if data_list:
                data_list = data_list.filter(Q(name__icontains=search_word) | Q(slogan__icontains=search_word)
                                               | Q(description__icontains=search_word) | Q(company__name=search_word)
                                               | Q(company__profile__user__first_name__icontains=search_word)
                                               | Q(company__profile__user__last_name__icontains=search_word)
                                               )
        if businnes_g:
            if data_list:
                data_list = data_list.filter(Q(businness_types__id=businnes_g) | Q(company__businnes_type__id=businnes_g)
                                                  )
        if regions_g:
            if data_list:
                data_list = data_list.filter(company__region=regions_g)
        else:
            data_list.filter(id=0)
    else:
        raise Http404
    if data_list:
        paginator = FlynsarmyPaginator(data_list, 30, adjacent_pages=3)  # Show 25 contacts per page

        page = request.GET.get('page') #page check is tam eded
        try:
            datas = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            datas = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            datas = paginator.page(paginator.num_pages)
    # else:
    context = {
        'datas':datas,
        'search_content':search_content,
        'search_word':search_word,
        'businnes_g':businnes_g,
        'regions_g':regions_g,
        'rand_events': rand_events,
        'rand_company_product_or_services': rand_company_product_or_services,
    }
    # return render(request, 'home/index.html', context=context)
    return render(request, 'home/search.html', context=context)




def busines_ajax(request,b_id):
    now = timezone.now()
    message_code = 0
    message= ''
    data = {'message_code': message_code, 'message': message}
    busines = Businnes.objects.filter(id=b_id).filter(active=True).order_by('order_index')
    if request.method == 'GET' and request.is_ajax():
        if busines:
            events = Event.objects.filter(company__businnes_type=busines).filter(deleted=False,is_active=True).filter(company__deleted=False,company__is_active=True)[:6]
            # companies = Company.objects.filter(businnes_type__id=busines.id)[:12]
            company_products = CompanyProductOrService.objects.filter(company__businnes_type=busines).filter(active=True).filter(deleted=False).filter(company__deleted=False,company__is_active=True)[:12]
            events_html_data = ''
            events_html_count = 0
            companies_html_data = ''
            companies_html_count = 0
            company_products_html_data = ''
            company_products_html_count = 0
            message_code = 1
            event_for = 1
            company_product_for = 1
            # event_for_div = False
            if events:
                try:
                    for event_o in events:
                        if event_o:
                            event_for_div = False
                            events_html_count += 1
                            event_id = str(event_o.id)
                            event_name = str(event_o.name)
                            event_company_name = str(event_o.company.name)
                            event_end_date = event_o.end_date
                            event_start_date = event_o.start_date
                            event_description = event_o.description
                            if int(event_for) % int(3) == 0:
                                event_for_div = True
                            event_for += 1
                            dif_= False
                            if event_o.end_date > now:
                                dif_ =True
                            event_image = event_o.image
                            events_html_data = '{0}{1}'.format(events_html_data,
                                                         render_to_string('include/_html_data/events_html_data.html',
                                                                          {
                                                                              'event_id': str(event_id),
                                                                              'event_name': str(event_name),
                                                                              'event_end_date': str(event_end_date),
                                                                              'event_start_date': str(event_start_date),
                                                                              'event_description': str(event_description),
                                                                              'event_image': str(event_image),
                                                                              'dif_date': dif_,
                                                                              'event_for_div': event_for_div,
                                                                          }))
                except:
                    pass
            if company_products:
                for company_product in company_products:
                    company_product_for_div = False
                    if int(company_product_for) % int(3) == 0:
                        company_product_for_div = True
                    company_product_for += 1
                    company_products_html_data = '{0}{1}'.format(company_products_html_data,
                                                 render_to_string('include/_html_data/company_products_html_data.html',
                                                                  {
                                                                      'company_product': company_product,
                                                                      'company_product_for_div': company_product_for_div,
                                                                  }))
            data = {
                    'message_code': message_code,
                    'events_html_data': events_html_data,
                    'company_products_html_data':company_products_html_data
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")
        else:
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")
    else:
        raise Http404
    # return render(request, 'home/index.html', context=context)
    # return render(request, 'home/index.html', context=context)

