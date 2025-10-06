from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import pgettext_lazy

from apartments.models import Apartment

from .models import OrderItem


class OfflineBookingForm(forms.ModelForm):
    from_date_errors = {
        'required': pgettext_lazy('business owner create offline booking page error',
                                  'Arrival date is required.'),
        'invalid': pgettext_lazy('business owner create offline booking page error',
                                 'Arrival date has incorrect format.')
    }
    to_date_errors = {
        'required': pgettext_lazy('business owner create offline booking page error',
                                  'Departure date is required.'),
        'invalid': pgettext_lazy('business owner create offline booking page error',
                                 'Departure date has incorrect format.')
    }
    validation_errors = {
        'too_short': pgettext_lazy('business owner create offline booking page error',
                                   'Departure should be more than arrival for at least 1 day.'),
        'incorrect_apartment': pgettext_lazy('business owner create offline booking page error',
                                             'This apartment has no price category. It cannot be used in '
                                             'offline booking.')
    }

    from_date = forms.DateField(input_formats=['%d.%m.%Y'], widget=forms.DateInput(format='%d.%m.%Y'),
                                error_messages=from_date_errors)
    to_date = forms.DateField(input_formats=['%d.%m.%Y'], widget=forms.DateInput(format='%d.%m.%Y'),
                              error_messages=to_date_errors)
    apartment = forms.ModelChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):
        super(OfflineBookingForm, self).__init__(*args, **kwargs)
        self.fields['apartment'].queryset = Apartment.objects.filter(owner=user, origin__isnull=True,
                                                                     price_category__isnull=False)

    class Meta:
        model = OrderItem
        fields = ('from_date', 'to_date', 'offline_booking_note')

    def clean_apartment(self):
        apartment = self.cleaned_data.get('apartment')
        if apartment:
            try:
                price_category = apartment.price_category
            except ObjectDoesNotExist:
                raise forms.ValidationError(self.validation_errors['incorrect_apartment'])
        return apartment

    def clean(self):
        cleaned_data = super(OfflineBookingForm, self).clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        if from_date and to_date:
            diff = (to_date - from_date).days
            if diff < 1:
                raise forms.ValidationError(self.validation_errors['too_short'])
        return cleaned_data