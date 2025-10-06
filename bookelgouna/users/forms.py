# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm
from allauth.account.utils import user_pk_to_url_str, user_username
from allauth.utils import build_absolute_uri
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField

from django import forms
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from django.core.urlresolvers import reverse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from phonenumber_field.phonenumber import to_python
from phonenumbers import example_number, PhoneNumberFormat, format_number

from common.form_mixins import PhoneUniquenessMixin
from common.widgets import HiddenClearableFileInput
from common.utils import get_phone_prefix_or_empty_string_for, is_valid_for_libphonenumber

from .exceptions import WrongUserType
from .models import BusinessOwnerInfo, User, Country


class BaseUserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(BaseUserLoginForm, self).__init__(*args, **kwargs)
        self.fields['remember'].initial = True
        self.fields['login'].widget.attrs.pop('autofocus')


class EndUserLoginForm(BaseUserLoginForm):

    def clean(self):
        cleaned_data = super(EndUserLoginForm, self).clean()
        if self.user and not self.user.is_end_user():
            raise WrongUserType
        return cleaned_data


class BusinessLoginForm(BaseUserLoginForm):

    def clean(self):
        cleaned_data = super(BusinessLoginForm, self).clean()
        if self.user and not self.user.is_business_related_user():
            raise WrongUserType
        return cleaned_data


class BaseUserSignupForm(SignupForm):
    # general user custom fields
    phone = forms.CharField(label=_('Phone'))
    agree = forms.BooleanField(initial=True, required=True,
                               error_messages={'required': pgettext_lazy('signup agree field error', 'You should agree to continue.')})

    def __init__(self, *args, **kwargs):
        super(BaseUserSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop('autofocus')


class EndUserSignupForm(PhoneUniquenessMixin, BaseUserSignupForm):
    # end user custom fields
    country = LazyTypedChoiceField(countries)
    error_messages = {
        'invalid_phone': pgettext_lazy('end user signup phone field error', u'Incorrect phone.'),
        'invalid_phone_with_example': pgettext_lazy('end user signup phone field error with example',
                                                    u'Incorrect phone. Example: <bdo dir="ltr">%(example)s</bdo>'),
        'phone_not_unique': pgettext_lazy('end user signup phone field error', 'This phone is not unique.'),
    }

    def clean(self):
        super(EndUserSignupForm, self).clean()
        country_code = self.cleaned_data.get('country')
        phone_value = self.cleaned_data.get('phone')
        if phone_value:
            phone_number = to_python(phone_value)
            if phone_number and not phone_number.is_valid():
                if country_code and is_valid_for_libphonenumber(country_code):
                    example = format_number(example_number(country_code), PhoneNumberFormat.E164)
                    self.add_error('phone', forms.ValidationError(self.error_messages['invalid_phone_with_example'],
                                                                  code='invalid_phone_with_example',
                                                                  params={'example': example}
                    ))
                else:
                    self.add_error('phone', forms.ValidationError(self.error_messages['invalid_phone'],
                                                                  code='invalid_phone'
                    ))


class BusinessSignupForm(PhoneUniquenessMixin, BaseUserSignupForm):
    COUNTRY_CODE = 'EG'
    COUNTRY_NAME = countries.name(COUNTRY_CODE)

    service_type_error_messages = {
        'required': pgettext_lazy('business owner signup business type error',
                                  'You should choose something to continue.')
    }

    # business owner custom fields
    service_type = forms.ChoiceField(label=_('Service Type'), error_messages=service_type_error_messages,
                                     choices=[('', '---------')] + BusinessOwnerInfo.SERVICE_TYPES)
    # shows only the country name but the actual value is set to EG inside AccountAdapter regardless of this field value
    country = forms.CharField(label=_('Country'), initial=COUNTRY_NAME, required=False)

    error_messages = {
        'invalid_phone': pgettext_lazy('business owner signup phone field error',
                                       u'Incorrect phone. Example: %(example)s'),
        'phone_not_unique': pgettext_lazy('business owner signup phone field error', 'This phone is not unique.'),
    }

    def __init__(self, *args, **kwargs):
        super(BusinessSignupForm, self).__init__(*args, **kwargs)

        self.fields['country'].widget.attrs['readonly'] = True
        self.fields['phone'].initial = get_phone_prefix_or_empty_string_for(self.COUNTRY_CODE)

    def clean_country(self):
        return self.COUNTRY_NAME

    def clean(self):
        super(BusinessSignupForm, self).clean()
        phone_value = self.cleaned_data.get('phone')
        if phone_value:
            phone_number = to_python(phone_value)
            if phone_number and not phone_number.is_valid():
                example = format_number(example_number(self.COUNTRY_CODE), PhoneNumberFormat.E164)
                self.add_error('phone', forms.ValidationError(self.error_messages['invalid_phone'],
                                                              code='invalid_phone',
                                                              params={'example': example}
                ))


class ProfileEditForm(forms.ModelForm):
    phone = forms.CharField(label=_('Phone'))

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget = HiddenClearableFileInput()
        self.fields['phone'].required = True


class EndUserProfileEditForm(PhoneUniquenessMixin, ProfileEditForm):
    error_messages = {
        'invalid_phone': pgettext_lazy('end user edit profile phone field error', u'Incorrect phone.'),
        'invalid_phone_with_example': pgettext_lazy('end user edit profile phone field error with example',
                                                    u'Incorrect phone. Example: <bdo dir="ltr">%(example)s</bdo>'),
        'phone_not_unique': pgettext_lazy('end user edit profile phone field error', 'This phone is not unique.'),
    }

    def clean(self):
        super(EndUserProfileEditForm, self).clean()
        country_code = self.cleaned_data.get('country')
        phone_value = self.cleaned_data.get('phone')
        if phone_value:
            phone_number = to_python(phone_value)
            if phone_number and not phone_number.is_valid():
                if country_code and is_valid_for_libphonenumber(country_code):
                    example = format_number(example_number(country_code), PhoneNumberFormat.E164)
                    self.add_error('phone', forms.ValidationError(self.error_messages['invalid_phone_with_example'],
                                                                  code='invalid_phone_with_example',
                                                                  params={'example': example}
                    ))
                else:
                    self.add_error('phone', forms.ValidationError(self.error_messages['invalid_phone'],
                                                                  code='invalid_phone'
                    ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'country', 'preferred_language', 'avatar', 'cropping')


class EndUserAddPhoneForm(PhoneUniquenessMixin, forms.ModelForm):
    COUNTRY_CODE = 'EG'

    phone = forms.CharField(label=_('Phone'))

    error_messages = {
        'invalid_phone': pgettext_lazy('end user checkout phone field error',
                                       u'Incorrect phone. Example: %(example)s'),
        'phone_not_unique': pgettext_lazy('end user checkout phone field error', 'This phone is not unique.'),
    }

    def __init__(self, *args, **kwargs):
        super(EndUserAddPhoneForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = True

    def clean(self):
        super(EndUserAddPhoneForm, self).clean()
        phone_value = self.cleaned_data.get('phone')
        if phone_value:
            phone_number = to_python(phone_value)
            if phone_number and not phone_number.is_valid():
                example = format_number(example_number(self.COUNTRY_CODE), PhoneNumberFormat.E164)
                self.add_error('phone', forms.ValidationError(self.error_messages['invalid_phone'],
                                                              code='invalid_phone',
                                                              params={'example': example}
                ))

    class Meta:
        model = User
        fields = ('phone',)


class BusinessProfileEditForm(PhoneUniquenessMixin, ProfileEditForm):
    COUNTRY_CODE = 'EG'

    error_messages = {
        'invalid_phone': pgettext_lazy('business owner edit profile phone field error',
                                       u'Incorrect phone. Example: %(example)s'),
        'phone_not_unique': pgettext_lazy('business onwer edit profile phone field error', 'This phone is not unique.'),
    }

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'preferred_language', 'phone', 'avatar', 'cropping')

    def clean(self):
        super(BusinessProfileEditForm, self).clean()
        phone_value = self.cleaned_data.get('phone')
        if phone_value:
            phone_number = to_python(phone_value)
            if phone_number and not phone_number.is_valid():
                example = format_number(example_number(self.COUNTRY_CODE), PhoneNumberFormat.E164)
                self.add_error('phone', forms.ValidationError(self.error_messages['invalid_phone'],
                                                              code='invalid_phone',
                                                              params={'example': example}
                ))


class BusinessResetPasswordForm(ResetPasswordForm):

    def save(self, request, **kwargs):

        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator",
                                     default_token_generator)

        for user in self.users:

            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            current_site = Site.objects.get_current()

            # resolve correct url according to user type
            if user.is_business_owner():
                url = "business_reset_password_from_key"
            else:
                url = "account_reset_password_from_key"

            # send the password reset email
            path = reverse(url, kwargs=dict(uidb36=user_pk_to_url_str(user), key=temp_key))
            url = build_absolute_uri(request, path, protocol=app_settings.DEFAULT_HTTP_PROTOCOL)
            context = {"site": current_site,
                       "user": user,
                       "password_reset_url": url}
            if app_settings.AUTHENTICATION_METHOD \
                    != app_settings.AuthenticationMethod.EMAIL:
                context['username'] = user_username(user)
            get_adapter().send_mail('account/email/password_reset_key',
                                    email,
                                    context)
        return self.cleaned_data["email"]


class SubaccountForm(forms.ModelForm):
    title = forms.CharField(label=pgettext_lazy('business onwer create subaccount title label', 'Display title for you'),
                            required=False, max_length=30)
    service_type = forms.ChoiceField(choices=BusinessOwnerInfo.SERVICE_TYPES, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user')
        super(SubaccountForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(SubaccountForm, self).save(commit=False)
        user.type = User.BUSINESS_OWNER
        user.country = 'EG'
        title = self.cleaned_data.get('title')
        if title:
            user.first_name = title
        user.set_unusable_password()
        user.save()
        base_account = self.current_user.get_base_account_or_self()
        base_account.subaccounts.add(user)
        service_type = self.cleaned_data.get('service_type')
        BusinessOwnerInfo.objects.create(user=user, service_type=service_type)
        return user

    class Meta:
        model = User
        fields = ('username',)
        labels = {
            'username': pgettext_lazy('business owner create subaccount identifier label', 'Unique identifier'),
        }
        error_messages = {
            'username': {
                'unique': pgettext_lazy('business owner create subaccount identifier error', 'This identifier is not unique.'),
            },
        }

