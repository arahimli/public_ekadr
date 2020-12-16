from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
# from social_auth.backends.pipeline import user

from multiupload.fields import MultiImageField, MultiFileField
from company.models import *
from general.models import Region
from payment.models import Currency
from registration.models import *
from geoposition.forms import GeopositionField
from django.utils.translation import ugettext as _
class AdminCompanyConfirm(forms.Form):
    is_active = forms.BooleanField(required=False)

class AdminProfileConfirm(forms.Form):
    is_active = forms.BooleanField(required=False)

AdminConfirmCHOICES=[('confirm',_('confirm')),
         ('reject',_('reject'))]
class AdminConfirmRejectedProfileConfirm(forms.Form):
    is_confirm = forms.ChoiceField(required=True,choices=AdminConfirmCHOICES,widget=forms.RadioSelect())


class ChangeProfileInfoForm(forms.Form):
    first_name = forms.CharField(max_length=255,min_length=2,required=True)
    last_name = forms.CharField(max_length=255,min_length=2,required=True)
    username = forms.CharField(max_length=255,min_length=5,required=True)
    email = forms.EmailField(required=True)
    type = forms.ChoiceField(required=False,choices=TYPECHOICES)
    voen = forms.CharField(max_length=255,min_length=6,required=False)
    bank_account = forms.CharField(max_length=255,min_length=6,required=False)
    region = forms.ChoiceField(choices=[],required=True)
    address = forms.CharField(required=False,max_length=255,min_length=2)
    businnes_types = forms.MultipleChoiceField(required=True,choices=[])
    businnes_types_parent = forms.MultipleChoiceField(required=False,choices=[])
    practices = forms.CharField(required=False,max_length=255,min_length=6,widget=forms.Textarea)
    password = forms.CharField(required=True,max_length=255,min_length=2,widget=forms.PasswordInput())
    def __init__(self,user_id,*args, **kwargs):
        super(ChangeProfileInfoForm, self).__init__(*args, **kwargs)
    #     self.user = kwargs.pop('user', None)
    #     print(self.user)
        regions_obj = Region.objects.filter()
        businnes_types_obj = Businnes.objects.filter(parent=None).filter(active=True)
        businnes_types_parent = Businnes.objects.exclude(parent=None).filter(active=True)
        businnes_types_choices = ()
        # for item in businnes_types_obj:
        #     businnes_types_choices.index()
        profile_o = Profile.objects.get(user_id=user_id)
        # if profile_o.type == ['admin-person']:
        #     self.fields['type'].choices = ONLYADMINTYPECHOICES
        self.fields['region'].choices = [[x.id, x.name] for x in regions_obj]

        self.fields['businnes_types'].choices = [[x.id, x.name] for x in businnes_types_obj]
        self.fields['businnes_types_parent'].choices = [[x.id, x.name] for x in businnes_types_parent]
    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        voen = cleaned_data.get('voen')
        bank_account = cleaned_data.get('bank_account')
        practices = cleaned_data.get('practices')
        address = cleaned_data.get('address')
        type = cleaned_data.get('type')
        # status = cleaned_data.get('status')
        businnes_types = cleaned_data.get('businnes_types')
        region = cleaned_data.get('region')
        # status_list = ['married','single','Widow']
        type_list = ['juridical-person','individual-person','ordinary-person']
        # user = User.objects.filter(username=username)
        # if User.objects.filter(username=username):
        #     self._errors['username'] = _('username_allready_use')
        # # user =
        # if User.objects.filter(email=email):
        #     self._errors['email'] = _('email_allready_use')
        if type:
            if type not in type_list:
                self._errors['type'] = _('type_is_incorrect')
        # if status not in status_list:
        #     self._errors['status'] = _('status_is_incorrect')
        if type:
            if type != 'ordinary-person':
                if not voen:
                    self._errors['voen'] = _('this_field_is_required')
                if not bank_account:
                    self._errors['bank_account'] = _('this_field_is_required')
                if not practices:
                    self._errors['practices'] = _('this_field_is_required')
                if not address:
                    self._errors['address'] = _('this_field_is_required.')
        if businnes_types:
            businnes_types_o = Businnes.objects.filter(id__in=businnes_types)
            if businnes_types_o.count() != len(businnes_types):
                self._errors['businnes_types'] = _('please_insert_correct_data.')
        if region:
            region_o = Region.objects.filter(id=region)
            if not region_o:
                self._errors['region'] = _('please_insert_correct_data.')
        password = cleaned_data.get('password')

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=255,min_length=2,required=True,widget=forms.PasswordInput())
    new_password = forms.CharField(max_length=255,min_length=8,required=True,widget=forms.PasswordInput())
    repeat_password = forms.CharField(max_length=255,min_length=8,required=True,widget=forms.PasswordInput())
    def clean(self):
        cleaned_data = self.cleaned_data
        new_password = cleaned_data.get('new_password')
        repeat_password = cleaned_data.get('repeat_password')
        # if len(new_password) <=7:
        #     self._errors['new_password'] = 'password_greater_than_7'
        # if len(repeat_password) <=7:
        #     self._errors['repeat_password'] = 'password_greater_than_7'
        if new_password != repeat_password:
            self._errors['repeat_password'] = 'passwords_not same'
        # print(identified)



class ChangePhotoForm(forms.Form):
    image = forms.ImageField(required=True)


class BusinnesTypeForm(forms.Form):
    businnes_type = forms.ChoiceField(choices=[], required=True)
    businnes_types_parent = forms.ChoiceField(choices=[],required=False)
    def __init__(self,*args, **kwargs):
        super(BusinnesTypeForm, self).__init__(*args, **kwargs)
        businnes_types_obj = Businnes.objects.filter(active=True).filter(parent=None).order_by('order_index')

        businnes_types_parent = Businnes.objects.exclude(parent=None).filter(active=True)
        self.fields['businnes_types_parent'].choices = [[x.id, x.name] for x in businnes_types_parent]

        self.fields['businnes_type'].choices = [[x.id, x.name] for x in businnes_types_obj]


class BusinnesTypeYearForm(forms.Form):
    businnes_type_year = forms.ChoiceField(choices=[], required=False)
    businnes_types_parent_year = forms.ChoiceField(choices=[],required=False)
    year = forms.ChoiceField(choices=[],required=True)
    def __init__(self,*args, **kwargs):
        super(BusinnesTypeYearForm, self).__init__(*args, **kwargs)
        businnes_types_obj = Businnes.objects.filter(active=True).filter(parent=None).order_by('order_index')
        now = timezone.now()
        default_year = 2017
        business_year_list = []
        if int(now.year) == default_year:
            business_year_list.append([default_year,default_year])
        else:
            if int(now.year) - default_year < 11:
                for x in range(default_year, now.year + 1):
                    business_year_list.append([x,x])
            else:
                for x in range(int(now.year) - 10, int(now.year + 1)):
                    business_year_list.append([x,x])
        businnes_types_parent = Businnes.objects.exclude(parent=None).filter(active=True)
        self.fields['businnes_types_parent_year'].choices = [[x.id, x.name] for x in businnes_types_parent]
        self.fields['businnes_type_year'].choices = [[x.id, x.name] for x in businnes_types_obj]
        self.fields['year'].choices = business_year_list

class CompanyCreateForm(forms.Form):
    name = forms.CharField(max_length=255,required=True)
    logo = forms.ImageField(required=True)
    cover_photo = forms.ImageField(required=True)
    slogan = forms.CharField(max_length=255,required=True)
    # is_active = forms.BooleanField(required=False)
    email = forms.EmailField()
    phones = forms.CharField(max_length=255,required=True)
    voen = forms.CharField(max_length=255,required=True)
    bank_account = forms.CharField(max_length=255,required=True)
    attachments = MultiFileField(min_num=1, max_num=7, max_file_size=1024*1024*5)
    region = forms.ChoiceField(choices=[], required=True)
    address = forms.CharField(max_length=255,required=True)
    businnes_type = forms.MultipleChoiceField(choices=[], required=True)
    businnes_types_parent = forms.MultipleChoiceField(choices=[],required=False)
    position = GeopositionField()
    practices = forms.CharField(widget=forms.Textarea,required=True)
    def __init__(self,user,*args, **kwargs):
        super(CompanyCreateForm, self).__init__(*args, **kwargs)
        self.user = kwargs.pop('user', None)
        print(self.user)
        regions_obj = Region.objects.filter()
        businnes_types_obj = Businnes.objects.filter(active=True).filter(parent=None)

        businnes_types_parent = Businnes.objects.exclude(parent=None).filter(active=True)
        self.fields['businnes_types_parent'].choices = [[x.id, x.name] for x in businnes_types_parent]
        self.fields['region'].choices = [[x.id, x.name] for x in regions_obj]
        self.fields['businnes_type'].choices = [[x.id, x.name] for x in businnes_types_obj]




class CompanyEditForm(forms.Form):
    name = forms.CharField(max_length=255,required=True)
    logo = forms.ImageField(required=False)
    cover_photo = forms.ImageField(required=False)
    slogan = forms.CharField(max_length=255,required=True)
    # is_active = forms.BooleanField(required=False)
    email = forms.EmailField()
    phones = forms.CharField(max_length=255,required=True)
    voen = forms.CharField(max_length=255,required=True)
    bank_account = forms.CharField(max_length=255,required=True)
    attachments = MultiFileField(min_num=1, max_num=7, max_file_size=1024*1024*5,required=False)
    region = forms.ChoiceField(choices=[], required=True)
    address = forms.CharField(max_length=255,required=True)
    businnes_type = forms.MultipleChoiceField(choices=[], required=True)
    businnes_types_parent = forms.MultipleChoiceField(choices=[],required=False)
    position = GeopositionField()
    practices = forms.CharField(widget=forms.Textarea,required=False)
    def __init__(self,*args, **kwargs):
        super(CompanyEditForm, self).__init__(*args, **kwargs)
        self.user = kwargs.pop('user', None)
        print(self.user)
        regions_obj = Region.objects.filter()
        businnes_types_obj = Businnes.objects.filter(active=True).filter(parent=None)
        businnes_types_parent = Businnes.objects.exclude(parent=None).filter(active=True)
        self.fields['businnes_types_parent'].choices = [[x.id, x.name] for x in businnes_types_parent]
        self.fields['region'].choices = [[x.id, x.name] for x in regions_obj]
        self.fields['businnes_type'].choices = [[x.id, x.name] for x in businnes_types_obj]



class CompanyProductOrServiceForm(forms.Form):
    # company = forms.ChoiceField(choices=[], required=True)
    type = forms.ChoiceField(required=True,choices=ProductOrServiceChoices,widget=forms.RadioSelect())
    product_or_service = forms.ChoiceField(choices=[], required=True)
    name = forms.CharField(max_length=255,required=True)
    logo = forms.ImageField(required=False)
    slogan = forms.CharField(max_length=255,required=True)
    is_active = forms.BooleanField(required=False)
    quantity = forms.DecimalField(max_digits=19, decimal_places=5,required=True)
    price = forms.DecimalField(max_digits=19, decimal_places=5,required=True)
    currency = forms.ChoiceField(choices=[], required=True)
    businnes_type = forms.MultipleChoiceField(choices=[], required=True)
    businnes_types_parent = forms.MultipleChoiceField(choices=[],required=False)
    # is_active = forms.BooleanField(label='is Publish')
    description = forms.CharField(widget=forms.Textarea,required=False)
    images = MultiImageField(min_num=0, max_num=13, max_file_size=1024*1024*5,required=False)
    # show_slider = forms.BooleanField(required=False)
    # meta_keywords = forms.CharField(max_length=100,required=False)
    # meta_description = forms.CharField(widget=forms.Textarea,required=False)
    # tags = forms.CharField(max_length=255, required=False)
    # identified_data = forms.CharField(max_length=255,widget=forms.HiddenInput())
    def __init__(self,*args, **kwargs):
        super(CompanyProductOrServiceForm, self).__init__(*args, **kwargs)
        # self.fields['categorys'].choices = [(x.pk, x.name) for x in Category.objects.all()]
        # userprofile = UserProfile.objects.filter(has_profile_page=True)
        # self.request = kwargs.pop('request')
        # request = self.request
        # user = self.request.user
        # user_profile = get_object_or_404(Profile,user=user)
        # companys_obj = Company.objects.filter(profile=user_profile)
        products_or_serices_obj = ProductOrService.objects.filter()
        currencies_obj = Currency.objects.filter()
        # categorys = self.categorys
        # print(self.fields['categorys'])
        # if categorys_list:
        #     categorys_obj.filter(id__in=categorys_list)
            # for category in categorys_list:
            #     categorys.filter(id__in=)
        # identified = self.fields['identified']
        # news_obj = News.objects.filter(unique_name=str(identified).strip())
        # self.fields['sponsors'].choices = [(x.pk, x.prof_sponsor_name) for x in userprofile]
        # self.fields['company'].choices = [[x.id, x.name] for x in companys_obj]
        businnes_types_obj = Businnes.objects.filter(active=True).filter(parent=None)
        businnes_types_parent = Businnes.objects.exclude(parent=None).filter(active=True)
        self.fields['businnes_types_parent'].choices = [[x.id, x.name] for x in businnes_types_parent]
        self.fields['businnes_type'].choices = [[x.id, x.name] for x in businnes_types_obj]
        self.fields['product_or_service'].choices = [[x.id, x.name] for x in products_or_serices_obj]
        self.fields['currency'].choices = [[x.id, x.name] for x in currencies_obj]
    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     unique_name = cleaned_data.get('unique_name')
    #     identified = cleaned_data.get('identified_data')
    #     # print(identified)
    #     if News.objects.filter(unique_name=unique_name).exists() and identified:
    #         self._errors['unique_name'] = unique_name +' '+ ' allready exists'
    #
    #     return cleaned_data
# class CompanyProductOrServiceImageForm(forms.ModelForm):
#     image = forms.ImageField(label='Image')
#     class Meta:
#         model = CompanyProductOrServiceImage
#         fields = ('image', )
# from bootstrap_datepicker.widgets import DateTimeInput
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget #- See more at: http://django-datetime-widget.asaglimbeni.me/model_form_v3/#sthash.gHmb0QHr.dpuf

class EventCreateForm(forms.Form):
    name = forms.CharField(max_length=255,required=True)
    company_product_or_service = forms.ChoiceField(choices=[], required=True)
    image = forms.ImageField(required=True)
    quantity = forms.DecimalField(max_digits=19, decimal_places=5,required=True)
    # price = forms.DecimalField(max_digits=19, decimal_places=5,required=True)
    currency = forms.ChoiceField(choices=[], required=True)

    # is_active = forms.BooleanField(label='is Publish')
    description = forms.CharField(widget=forms.Textarea,required=False)
    businnes_type = forms.MultipleChoiceField(choices=[], required=True)
    businnes_types_parent = forms.MultipleChoiceField(choices=[],required=False)
    is_active = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(required=True) #- See more at: http://django-datetime-widget.asaglimbeni.me/model_form_v3/#sthash.gHmb0QHr.dpuf
    end_date = forms.DateTimeField(required=True)
    position = GeopositionField()
    # show_slider = forms.BooleanField(required=False)
    # meta_keywords = forms.CharField(max_length=100,required=False)
    # meta_description = forms.CharField(widget=forms.Textarea,required=False)
    # tags = forms.CharField(max_length=255, required=False)
    # identified_data = forms.CharField(max_length=255,widget=forms.HiddenInput())
    def __init__(self,company_id,*args, **kwargs):
        super(EventCreateForm, self).__init__(*args, **kwargs)
        # self.fields['categorys'].choices = [(x.pk, x.name) for x in Category.objects.all()]
        # userprofile = UserProfile.objects.filter(has_profile_page=True)
        # self.request = kwargs.pop('request')
        # request = self.request
        # user = self.request.user
        # user_profile = get_object_or_404(Profile,user=user)
        # companys_obj = Company.objects.filter(profile=user_profile)

        currencies_obj = Currency.objects.filter()
        company_product_or_services_obj = CompanyProductOrService.objects.filter(company__id=company_id)
        # categorys = self.categorys
        # print(self.fields['categorys'])
        # if categorys_list:
        #     categorys_obj.filter(id__in=categorys_list)
            # for category in categorys_list:
            #     categorys.filter(id__in=)
        # identified = self.fields['identified']
        # news_obj = News.objects.filter(unique_name=str(identified).strip())
        # self.fields['sponsors'].choices = [(x.pk, x.prof_sponsor_name) for x in userprofile]
        # self.fields['company'].choices = [[x.id, x.name] for x in companys_obj]
        businnes_types_obj = Businnes.objects.filter(active=True).filter(parent=None)
        businnes_types_parent = Businnes.objects.exclude(parent=None).filter(active=True)
        self.fields['businnes_types_parent'].choices = [[x.id, x.name] for x in businnes_types_parent]
        self.fields['businnes_type'].choices = [[x.id, x.name] for x in businnes_types_obj]
        self.fields['currency'].choices = [[x.id, x.name] for x in currencies_obj]
        self.fields['company_product_or_service'].choices = [[x.id, x.name] for x in company_product_or_services_obj]



class EventEditForm(forms.Form):
    name = forms.CharField(max_length=255,required=True)
    company_product_or_service = forms.ChoiceField(choices=[], required=True)
    image = forms.ImageField(required=False)
    quantity = forms.DecimalField(max_digits=19, decimal_places=5,required=True)
    # price = forms.DecimalField(max_digits=19, decimal_places=5,required=True)
    currency = forms.ChoiceField(choices=[], required=True)

    # is_active = forms.BooleanField(label='is Publish')
    description = forms.CharField(widget=forms.Textarea,required=False)
    businnes_type = forms.MultipleChoiceField(choices=[], required=True)
    businnes_types_parent = forms.MultipleChoiceField(choices=[],required=False)
    is_active = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(required=True) #- See more at: http://django-datetime-widget.asaglimbeni.me/model_form_v3/#sthash.gHmb0QHr.dpuf
    end_date = forms.DateTimeField(required=True)
    position = GeopositionField()
    # show_slider = forms.BooleanField(required=False)
    # meta_keywords = forms.CharField(max_length=100,required=False)
    # meta_description = forms.CharField(widget=forms.Textarea,required=False)
    # tags = forms.CharField(max_length=255, required=False)
    # identified_data = forms.CharField(max_length=255,widget=forms.HiddenInput())
    def __init__(self,company_id,*args, **kwargs):
        super(EventEditForm, self).__init__(*args, **kwargs)
        # self.fields['categorys'].choices = [(x.pk, x.name) for x in Category.objects.all()]
        # userprofile = UserProfile.objects.filter(has_profile_page=True)
        # self.request = kwargs.pop('request')
        # request = self.request
        # user = self.request.user
        # user_profile = get_object_or_404(Profile,user=user)
        # companys_obj = Company.objects.filter(profile=user_profile)
        currencies_obj = Currency.objects.filter()
        company_product_or_services_obj = CompanyProductOrService.objects.filter(company__id=company_id)
        # categorys = self.categorys
        # print(self.fields['categorys'])
        # if categorys_list:
        #     categorys_obj.filter(id__in=categorys_list)
            # for category in categorys_list:
            #     categorys.filter(id__in=)
        # identified = self.fields['identified']
        # news_obj = News.objects.filter(unique_name=str(identified).strip())
        businnes_types_obj = Businnes.objects.filter(active=True).filter(parent=None)
        self.fields['businnes_type'].choices = [[x.id, x.name] for x in businnes_types_obj]
        businnes_types_parent = Businnes.objects.exclude(parent=None).filter(active=True)
        self.fields['businnes_types_parent'].choices = [[x.id, x.name] for x in businnes_types_parent]
        self.fields['currency'].choices = [[x.id, x.name] for x in currencies_obj]
        self.fields['company_product_or_service'].choices = [[x.id, x.name] for x in company_product_or_services_obj]


# class ChangePasswordForm(forms.Form):
#     old_password = forms.CharField(max_length=255,widget=forms.PasswordInput())
#     new_password = forms.CharField(max_length=255,min_length=8,widget=forms.PasswordInput())
#     repeat_password = forms.CharField(max_length=255,min_length=8,widget=forms.PasswordInput())

