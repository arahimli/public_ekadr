from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

from .views import *


urlpatterns = [
	url(r'^log-out/$', log_out, name='log_out'),
	url(r'^sign-in/$', sign_in, name='sign_in'),
	url(r'^sign-up/$', sign_up, name='sign_up'),
	url(r'^forgot-password/$', forgot_password, name='forgot_password'),
	url(r'^parent-business-ajax$', parent_business_ajax, name='parent_business_ajax'),

    # url(r'^contact/$', 'home.views.contact',name='contact'),

]
