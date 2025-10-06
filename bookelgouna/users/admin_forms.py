# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.utils import email_address_exists
from multiselectfield import MultiSelectFormField

from django import forms

from .models import User, BusinessOwnerInfo


class TravelAgencyForm(forms.ModelForm):
    password = forms.CharField()
    allowed_types = MultiSelectFormField(choices=BusinessOwnerInfo.SERVICE_TYPES, initial=BusinessOwnerInfo.ALL_TYPES)

    def __init__(self, *args, **kwargs):
        super(TravelAgencyForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def save(self, commit=True):
        user = super(TravelAgencyForm, self).save(commit=False)
        user.type = User.TRAVEL_AGENCY
        user.country = 'EG'
        user.set_password(self.cleaned_data["password"])
        user.save()
        allowed_types = self.cleaned_data.get('allowed_types')
        EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)
        BusinessOwnerInfo.objects.create(user=user, service_type=BusinessOwnerInfo.AGENCY, allowed_types=allowed_types,
                                         show_next_link=False)
        return user

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        value = self.cleaned_data["email"]
        value = get_adapter().clean_email(value)
        if value and email_address_exists(value):
            raise forms.ValidationError("A user is already registered with this e-mail address.")
        return value
