from django import forms
from django.http import HttpResponse

from company.models import *
from payment.models import *
from multiupload.fields import MultiFileField

class EventAppealForm(forms.Form):
    company = forms.ChoiceField(choices=[], required=True)
    price = forms.DecimalField(max_digits=19, decimal_places=5,required=True)
    attachments = MultiFileField(min_num=1, max_num=7, max_file_size=1024*1024*5)

    # If you need to upload media files, you can use this:
    # attachments = MultiMediaField(
    #     min_num=1,
    #     max_num=3,
    #     max_file_size=1024*1024*5,
    #     media_type='video'  # 'audio', 'video' or 'image'
    # )
    currency = forms.ChoiceField(choices=[], required=True)

    def __init__(self,user_id,e_company_id,*args, **kwargs):
        super(EventAppealForm, self).__init__(*args, **kwargs)
        companies_o = Company.objects.filter(profile__user_id=user_id).filter(is_active=True,deleted=False).exclude(id=e_company_id)
        currencies_obj = Currency.objects.filter()
        self.fields['company'].choices = [[x.id, x.name] for x in companies_o]
        self.fields['currency'].choices = [[x.id, x.name] for x in currencies_obj]

    def clean(self):
        cleaned_data = self.cleaned_data
        currency = cleaned_data.get('currency')
        company = cleaned_data.get('company')

        if company:
            company_o = Company.objects.filter(id=company).filter(is_active=True,deleted=False)
            if company_o.count() == 0:
                self._errors['company'] = 'please_select_correct_data'

        if currency:
            currency_o = Currency.objects.filter(id=currency)
            if currency_o.count() == 0:
                self._errors['currency'] = 'please_select_correct_data'

        # if company_o
        # company = cleaned_data.get('company')
        # identified = cleaned_data.get('identified_data')
        # print(identified)

        return cleaned_data