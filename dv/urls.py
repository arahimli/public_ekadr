from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

from .views import *


urlpatterns = [
	url(r'^dv/$', index, name='dv'),
    # url(r'^contact/$', 'home.views.contact',name='contact'),

]
