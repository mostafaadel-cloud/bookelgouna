from extra_views import InlineFormSet
from hvad.forms import BaseTranslationFormSet, translationformset_factory

from django import forms
from django.conf import settings
from django.forms import BaseInlineFormSet
from django.utils import timezone
from django.utils.datastructures import OrderedSet
from django.utils.translation import ugettext as _

from .fields import TypedImageField
from .models import TempFile
from .utils import default_arrival_date, default_departure_date


class TravelDatesForm(forms.Form):

    arrival_errors = {
        'required': _('Arrival date is required.'),
        'invalid': _('Arrival date has incorrect format.')
    }
    departure_errors = {
        'required': _('Departure date is required.'),
        'invalid': _('Departure date has incorrect format.')
    }
    dates_errors = {
        'too_short': _('Departure should be more than arrival for at least 1 day.'),
        'too_wide': _('You cannot book something for more than 30 days.'),
        'too_early': _('You cannot book earlier than half a year before.'),
    }

    arrival = forms.DateField(input_formats=['%d.%m.%Y'], widget=forms.DateInput(format='%d.%m.%Y'),
                              error_messages=arrival_errors)
    departure = forms.DateField(input_formats=['%d.%m.%Y'], widget=forms.DateInput(format='%d.%m.%Y'),
                                error_messages=departure_errors)

    def clean(self):
        cleaned_data = super(TravelDatesForm, self).clean()
        arrival = cleaned_data.get('arrival')
        departure = cleaned_data.get('departure')
        if arrival and departure:
            diff = (departure - arrival).days
            if diff < 1:
                raise forms.ValidationError(self.dates_errors['too_short'])
            elif diff > 30:
                raise forms.ValidationError(self.dates_errors['too_wide'])
            else:
                today = timezone.now().date()
                diff_from_today = (arrival - today).days
                if diff_from_today > 182:
                    raise forms.ValidationError(self.dates_errors['too_early'])
        return cleaned_data


class DatesAndGuestsForm(TravelDatesForm):
    ADULTS_CHOICES = ((x, x) for x in range(1, 5))
    CHILDREN_CHOICES = ((x, x) for x in range(0, 4))
    adults = forms.ChoiceField(choices=ADULTS_CHOICES, initial=2)
    children = forms.ChoiceField(choices=CHILDREN_CHOICES, initial=0)

    @staticmethod
    def default_data():
        return {
            'arrival': default_arrival_date(),
            'departure': default_departure_date(),
            'adults': 2,
            'children': 0
        }


class DatesAndGuestsAjaxForm(DatesAndGuestsForm):
    pass


class DatesAndGuestsPostForm(DatesAndGuestsForm):
    dates_errors = {
        'too_short': _('Departure should be more than arrival for at least 1 day. 7-days interval from today is used.'),
        'too_wide': _('You cannot book something for more than 30 days. 7-days interval from today is used.'),
        'too_early': _('You cannot book earlier than half a year before. 7-days interval from today is used.'),
    }


class TranslationsBaseInline(InlineFormSet):
    main_model = None
    max_num = len(settings.LANGUAGES)
    extra = len(settings.LANGUAGES)
    # this formset guarantees that at least one translation was added
    formset_class = BaseTranslationFormSet

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        super(TranslationsBaseInline, self).__init__(self.main_model, request, instance, view_kwargs, view)

    def get_formset(self):
        return translationformset_factory(self.model, **self.get_factory_kwargs())

    def construct_formset(self):
        # hack: skip InlineFormSet.construct_formset() method invocation and call BaseFormSetMixin version
        return super(InlineFormSet, self).construct_formset()

    def get_initial(self):
        extra_langs = OrderedSet([lang[0] for lang in settings.LANGUAGES])
        if self.object:
            for existing_lang in self.object.get_available_languages():
                extra_langs.remove(existing_lang)
        initial = [{'language_code': lang} for lang in extra_langs]
        return initial


class TimeBasedItemDiscountInlineFormSet(BaseInlineFormSet):

    def clean(self):
        super(TimeBasedItemDiscountInlineFormSet, self).clean()

        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        forms_and_number_of_days = []
        for form in self.forms:
            number_of_days = form.cleaned_data.get('number_of_days')
            if number_of_days:
                form_and_number_of_days = {
                    'form': form,
                    'number_of_days': number_of_days,
                }
                forms_and_number_of_days.append(form_and_number_of_days)
        if len(forms_and_number_of_days) > 1:
            clash = False
            for form_and_number1 in forms_and_number_of_days:
                for form_and_number2 in forms_and_number_of_days:
                    if form_and_number1['form'] == form_and_number2['form']:
                        continue
                    n1 = form_and_number1['number_of_days']
                    n2 = form_and_number2['number_of_days']
                    if n1 == n2:
                        # partial clash
                        f1 = form_and_number1['form']
                        f2 = form_and_number2['form']
                        f1.add_error('number_of_days', _('This value should be unique.'))
                        f2.add_error('number_of_days', _('This value should be unique.'))
                        clash = True
            if clash:
                raise forms.ValidationError(_("Non-unique numbers of days were found (outlined by red)"))


class ImageFieldValidationForm(forms.Form):
    image = TypedImageField()


class FeaturedImageForm(forms.Form):
    featured_image = forms.ImageField(label=_("Add featured image"), required=False, widget=forms.FileInput)


class MultipleImagesForm(forms.Form):
    multiple_images = forms.ImageField(label=_("Add pictures"), required=False, widget=forms.FileInput)


class TempImageForm(forms.ModelForm):
    image = TypedImageField()

    class Meta:
        model = TempFile
        fields = ('image',)


class DatetimeForm(forms.Form):
    datetime = forms.DateTimeField(input_formats=['%d.%m.%Y %H:%M'],
                                   widget=forms.DateTimeInput(format='%d.%m.%Y %H:%M'))
