from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

from .views import *


urlpatterns = [
	url(r'^$', index, name='index'),
	url(r'^faq/$', faq, name='faq'),
	url(r'^search/(?P<sc_slug>[\w-]+)/$', search, name='search'),
	url(r'^ajax-busines/(?P<b_id>[\w-]+)/$', busines_ajax, name='busines_ajax'),
    # url(r'^contact/$', 'home.views.contact',name='contact'),

]
