from django import forms
from django.http import HttpResponse

from company.models import *
from general.models import Region
from payment.models import *
from multiupload.fields import MultiFileField

class HomeSearchForm(forms.Form):
    search = forms.CharField(max_length=255, required=False)
    businnes = forms.ChoiceField(choices=[], required=False)
    regions = forms.ChoiceField(choices=[], required=False)

    def __init__(self,*args, **kwargs):
        super(HomeSearchForm, self).__init__(*args, **kwargs)
        regions = Region.objects.filter()
        businnes_types_obj = Businnes.objects.filter(active=True)

        self.fields['regions'].choices = [[x.id, x.name] for x in regions]
        self.fields['businnes'].choices = [[x.id, x.name] for x in businnes_types_obj]

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     search = cleaned_data.get('search')
    #     company = cleaned_data.get('company')
        # currency_o = Currency.objects.filter(id=currency)
        # company_o = Company.objects.filter(id=company).filter(is_active=True,deleted=False)
        # if currency_o.count() == 0:
        #     self._errors['currency'] = 'please_select_correct_data'
        # if company_o.count() == 0:
        #     self._errors['company'] = 'please_select_correct_data'
        # # company = cleaned_data.get('company')
        # # identified = cleaned_data.get('identified_data')
        # # print(identified)

        # return cleaned_data