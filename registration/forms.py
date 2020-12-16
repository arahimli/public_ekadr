from django import forms
from django.contrib.auth.models import User
from nocaptcha_recaptcha.fields import NoReCaptchaField

from django.utils.translation import ugettext as _

from company.models import Businnes
from general.models import Region


class BusinnesTypesForm(forms.Form):
    businnes_types = forms.MultipleChoiceField(choices=[],required=True)
    # def __init__(self,*args, **kwargs):
    #     super(BusinnesTypesForm, self).__init__(*args, **kwargs)
    #     businnes_types_obj = Businnes.objects.filter(parent=None)
    #     self.fields['businnes_types'].choices = [[x.id, x.name] for x in businnes_types_obj]
        # print(identified)




class LoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=255,min_length=2,required=True)
    password = forms.CharField(max_length=255,required=True,widget=forms.PasswordInput())
    remember_me = forms.BooleanField(required=False)
    # captcha = NoReCaptchaField(gtag_attrs={'data-theme': 'light'})
    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     new_password = cleaned_data.get('new_password')
    #     repeat_password = cleaned_data.get('repeat_password')
    #     # if len(new_password) <=7:
    #     #     self._errors['new_password'] = 'password_greater_than_7'
    #     # if len(repeat_password) <=7:
    #     #     self._errors['repeat_password'] = 'password_greater_than_7'
    #     if new_password != repeat_password:
    #         self._errors['repeat_password'] = 'passwords_not same'
    #     # print(identified)


STATUS_CHOICES = (
    ('married', _("married")),
    ('single', _("single")),
    ('widow', _("widow")),
)
TYPECHOICES = (
    ('juridical-person', _("juridical_person")),
    ('individual-person', _("individual_person")),
    ('ordinary-person', _("ordinary_person")),
)

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=255,min_length=2,required=True)
    last_name = forms.CharField(max_length=255,min_length=2,required=True)
    username = forms.CharField(max_length=255,min_length=5,required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=255,min_length=8, required=True, widget=forms.PasswordInput())
    repeat_password = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput())
    type = forms.ChoiceField(required=True,choices=TYPECHOICES)
    voen = forms.CharField(max_length=255,min_length=6,required=False)
    bank_account = forms.CharField(max_length=255,min_length=6,required=False)
    region = forms.ChoiceField(choices=[],required=True)
    address = forms.CharField(max_length=255,min_length=2,required=False)
    businnes_types = forms.MultipleChoiceField(choices=[],required=True)
    businnes_types_parent = forms.MultipleChoiceField(choices=[],required=False)
    practices = forms.CharField(max_length=255,min_length=6,required=False,widget=forms.Textarea)
    captcha = NoReCaptchaField(gtag_attrs={'data-theme': 'light'})
    def __init__(self,*args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
    #     self.user = kwargs.pop('user', None)
    #     print(self.user)
        regions_obj = Region.objects.filter()
        businnes_types_obj = Businnes.objects.filter(parent=None).filter(active=True)
        businnes_types_parent = Businnes.objects.exclude(parent=None).filter(active=True)
        businnes_types_choices = ()
        # for item in businnes_types_obj:
        #     businnes_types_choices.index()
        self.fields['region'].choices = [[x.id, x.name] for x in regions_obj]

        self.fields['businnes_types'].choices = [[x.id, x.name] for x in businnes_types_obj]
        self.fields['businnes_types_parent'].choices = [[x.id, x.name] for x in businnes_types_parent]
    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
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
        user_username = User.objects.filter(username=username)
        user_email = User.objects.filter(username=email)
        if user_username:
            self._errors['username'] = _('username_allready_use')
        # user =
        if user_email:
            self._errors['email'] = _('email_allready_use')
        if type not in type_list:
            self._errors['type'] = _('type_is_incorrect')
        # if status not in status_list:
        #     self._errors['status'] = _('status_is_incorrect')
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
        repeat_password = cleaned_data.get('repeat_password')
        if password != repeat_password:
            self._errors['repeat_password'] = _('passwords_not same')
        # print(identified)
        return cleaned_data



class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = NoReCaptchaField(gtag_attrs={'data-theme': 'light'})
    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
        except:
            self._errors['email'] = _('not_user_with_this_email')

        return cleaned_data