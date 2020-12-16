from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

from .views import *


urlpatterns = [
	url(r'^companies/$', companies, name='companies'),
	url(r'^company/(?P<c_id>[\w-]+)/$', company, name='company'),
	url(r'^company-pagination-content/(?P<c_id>[\w-]+)/(?P<content_slug>[\w-]+)/(?P<p_number>[0-9]+)/$', company, name='company'),
	url(r'^company/product/(?P<cp_id>[\w-]+)/$', company_product_or_service, name='company_product_or_service'),
	url(r'^events/$', events, name='events'),
	url(r'^events/(?P<e_id>[0-9]+)/$', event, name='event'),
	url(r'^busines/(?P<b_id>[\w-]+)/(?P<bc_slug>[\w-]+)/$', busines, name='busines'),
	url(r'^add-cart-ajax/(?P<ps_id>[\w-]+)/$', add_cart_ajax, name='add_cart_ajax'),
    # url(r'^contact/$', 'home.views.contact',name='contact'),

]
