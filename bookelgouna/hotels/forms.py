from django.core import validators
from django.db.models import Prefetch
from extra_views import InlineFormSet
from image_cropping import ImageCropWidget

from django import forms
from django.forms import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

from booking.models import CartItem
from common.form_mixins import FeaturedImageFormMixin, MultipleImagesFormMixin
from common.forms import TravelDatesForm, TranslationsBaseInline
from common.models import TempFile


from .models import Hotel, HotelImage, Room, RoomPrice, HotelComment, RoomPriceCategory, RoomType, MealPlan, \
    HotelAmenity, HotelAmenityCategory, RoomAmenity, HotelReview
from .widgets import CheckboxSelectMultipleIter


class HotelImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HotelImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = forms.FileInput()

    class Meta:
        model = HotelImage
        fields = ('image',)


class HotelImageInline(InlineFormSet):
    form_class = HotelImageForm
    model = HotelImage
    main_model = Hotel
    extra = 0

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        super(HotelImageInline, self).__init__(self.main_model, request, instance, view_kwargs, view)

    class Meta:
        fields = ('image',)


class HotelTranslationsInline(TranslationsBaseInline):
    main_model = Hotel

    class Meta:
        fields = ('title', 'long_description')


class HotelForm(FeaturedImageFormMixin, MultipleImagesFormMixin, forms.ModelForm):
    image_model = HotelImage

    amenities = forms.ModelMultipleChoiceField(
        queryset=HotelAmenity.objects.language().fallbacks().prefetch_related('translations').prefetch_related(Prefetch('category', queryset=HotelAmenityCategory.objects.language().fallbacks())),
        widget=CheckboxSelectMultipleIter,
        required=False
    )
    featured_image_pk = forms.IntegerField(label=_('Featured Image'), required=False, min_value=1)
    multiple_image_pk = forms.CharField(required=False, validators=[validators.validate_comma_separated_integer_list])
    error_messages = {
        'no_featured_image': pgettext_lazy('hotel error message on business owner page',
                                           'No featured image.')
    }

    class Meta:
        model = Hotel
        fields = ('address', 'rating', 'amenities')


class RoomPriceForm(forms.ModelForm):
    from_date_errors = {
        'required': _('Start date is required.'),
        'invalid': _('Start date has incorrect format.')
    }
    to_date_errors = {
        'required': _('End date is required.'),
        'invalid': _('End date has incorrect format.')
    }
    price_errors = {
        'required': _('Price is required.'),
        'invalid': _('Price has incorrect format.')
    }
    from_date = forms.DateField(label=_('from'), input_formats=['%d.%m.%Y'], widget=forms.DateInput(format='%d.%m.%Y'),
                                error_messages=from_date_errors)
    to_date = forms.DateField(label=_('to (excl.)'), input_formats=['%d.%m.%Y'], widget=forms.DateInput(format='%d.%m.%Y'),
                              error_messages=to_date_errors)

    def __init__(self, *kwargs, **args):
        super(RoomPriceForm, self).__init__(*kwargs, **args)
        self.fields['price'].error_messages['required'] = self.price_errors['required']
        self.fields['price'].error_messages['invalid'] = self.price_errors['invalid']

    def clean_to_date(self):
        cleaned_data = self.cleaned_data
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        if from_date and to_date:
            diff = (to_date - from_date).days
            if diff < 1:
                raise forms.ValidationError(_('End date should be more than start date.'))
        return to_date

    class Meta:
        model = RoomPrice
        fields = ('price', 'from_date', 'to_date')


# class CartItemForm(forms.ModelForm):
#     # content_type_pk = forms.IntegerField(min_value=1)
#     # item_pk = forms.IntegerField(min_value=1)
#     from_date = forms.DateField(input_formats=['%d.%m.%Y'], widget=forms.DateInput(format='%d.%m.%Y'))
#     to_date = forms.DateField(input_formats=['%d.%m.%Y'], widget=forms.DateInput(format='%d.%m.%Y'))
#
#     class Meta:
#         model = CartItem
#         fields = ('from_date', 'to_date')


class RoomInlineFormSet(BaseInlineFormSet):
    def get_queryset(self):
        """
        This is needed here instead of explicit filtering of room prices filter(generated=False).order_by('from_date')
        cause it doesn't work correctly. This filtering is done in RoomPriceCategoryUpdateView so instance
        contains prefetched correctly filtered and ordered prices.
        """
        return self.instance.prices.all()

    def clean(self):
        """ There are two possible situatians when price date ranges are clashed:
            1. One range fully includes another range. Lets find bigger and mark both of them as clashed.
            2. One range partially includes another range. Lets find earlier and mark both of therm as clashed
        """
        super(RoomInlineFormSet, self).clean()

        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        form_and_dateranges = []
        for form in self.forms:
            # skip autogenerated price ranges
            if hasattr(form.instance, 'pk') and form.instance.generated:
                continue
            start_date = form.cleaned_data.get('from_date')
            to_date = form.cleaned_data.get('to_date')
            if start_date and to_date:
                form_and_daterange = {
                    'form': form,
                    'start': start_date,
                    'end': to_date,
                }
                form_and_dateranges.append(form_and_daterange)
        if len(form_and_dateranges) > 1:
            clash = False
            for form_and_dates1 in form_and_dateranges:
                for form_and_dates2 in form_and_dateranges:
                    if form_and_dates1['form'] == form_and_dates2['form']:
                        continue
                    s1 = form_and_dates1['start']
                    e1 = form_and_dates1['end']
                    s2 = form_and_dates2['start']
                    e2 = form_and_dates2['end']
                    if s1 < s2 < e1 < e2:
                        # partial clash
                        f1 = form_and_dates1['form']
                        f2 = form_and_dates2['form']
                        f1.add_error(None, _('This daterange is clashed with some other daterange.'))
                        f2.add_error(None, _('This daterange is clashed with some other daterange.'))
                        clash = True
                    elif s1 <= s2 < e2 <= e1:
                        # full inclusion
                        f1 = form_and_dates1['form']
                        f2 = form_and_dates2['form']
                        f1.add_error(None, _('This daterange is clashed with some other daterange.'))
                        f2.add_error(None, _('This daterange is clashed with some other daterange.'))
                        clash = True
            if clash:
                raise forms.ValidationError(_("Clashed dateranges were found (outlined by red)"))


class RoomPriceCategoryPricesInline(InlineFormSet):
    main_model = RoomPriceCategory
    form_class = RoomPriceForm
    model = RoomPrice
    formset_class = RoomInlineFormSet
    extra = 100

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        super(RoomPriceCategoryPricesInline, self).__init__(self.main_model, request, instance, view_kwargs, view)

    class Meta:
        fields = ('price', 'from_date', 'to_date')


class RoomPriceCategoryForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=RoomType.objects.prefetch_related('translations'), empty_label=None)
    meal_plan = forms.ModelChoiceField(queryset=MealPlan.objects.prefetch_related('translations'), empty_label=None)

    class Meta:
        model = RoomPriceCategory
        fields = ('type', 'regular_price', 'pay_option', 'meal_plan')
        widgets = {
            'pay_option': forms.RadioSelect(attrs={'class': 'cabinet__radiobox-input'}),
        }


class RoomTranslationsInline(TranslationsBaseInline):
    main_model = Room

    class Meta:
        fields = ('long_description',)


class RoomPriceCategoryTranslationsInline(TranslationsBaseInline):
    main_model = RoomPriceCategory

    class Meta:
        fields = ('name', 'conditions',)


class RoomForm(FeaturedImageFormMixin, forms.ModelForm):
    ADULTS_CHOICES = ((x, x) for x in range(1, 5))
    CHILDREN_CHOICES = ((x, x) for x in range(0, 4))
    adults = forms.ChoiceField(choices=ADULTS_CHOICES, initial=2)
    children = forms.ChoiceField(choices=CHILDREN_CHOICES, initial=0)
    amenities = forms.ModelMultipleChoiceField(
        queryset=RoomAmenity.objects.language().fallbacks().prefetch_related('translations'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    featured_image_pk = forms.IntegerField(label=_('Featured Image'), required=False, min_value=1)
    error_messages = {
        'no_featured_image': pgettext_lazy('room error message on business owner page',
                                           'No featured image.')
    }

    class Meta:
        model = Room
        fields = ('allotment', 'area',  'adults', 'children', 'has_sea_views',
                  'has_air_conditioning', 'show_on_site', 'amenities')


class HotelGalleryImageCropForm(forms.ModelForm):
    class Meta:
        model = HotelImage
        fields = ('image', 'big_crop', 'small_crop')
        widgets = {
            'image': ImageCropWidget,
        }


class HotelFeaturedImageCropForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ('featured_image', 'big_crop', 'small_crop')
        widgets = {
            'featured_image': ImageCropWidget,
        }


class RoomImageCropForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('featured_image', 'crop')
        widgets = {
            'featured_image': ImageCropWidget,
        }


class HotelSearchForm(forms.Form):
    rating = forms.ChoiceField(choices=Hotel.HOTEL_RATINGS, widget=forms.HiddenInput)
    from_price = forms.IntegerField(widget=forms.HiddenInput)
    to_price = forms.IntegerField(widget=forms.HiddenInput)
    page = forms.IntegerField(widget=forms.HiddenInput, initial=1)


class RoomSearchForm(TravelDatesForm):
    pass


class CartItemForm(forms.ModelForm):
    # content_type_pk = forms.IntegerField(min_value=1)
    # item_pk = forms.IntegerField(min_value=1)
    from_date = forms.DateField(input_formats=['%d.%m.%Y'], widget=forms.DateInput(format='%d.%m.%Y'))
    to_date = forms.DateField(input_formats=['%d.%m.%Y'], widget=forms.DateInput(format='%d.%m.%Y'))

    class Meta:
        model = CartItem
        fields = ('from_date', 'to_date')


class HotelCommentForm(forms.ModelForm):
    entity_id = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(HotelCommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = HotelComment
        fields = ('text',)

    def clean(self):
        entity_id = self.cleaned_data.get('entity_id')
        if entity_id:
            user = self.request.user
            if user.is_authenticated() and user.is_end_user():
                try:
                    Hotel.originals.get(id=entity_id)
                except Hotel.DoesNotExist:
                    raise forms.ValidationError(_('No hotel with this pk.'))
                if user.hotel_comments.filter(entity_id=entity_id).exists():
                    raise forms.ValidationError(_('You have added comment earlier. It might not have been approved yet.'))
            else:
                raise forms.ValidationError(_('Only authorized clients can add new comments.'))


class HotelReviewForm(forms.ModelForm):
    class Meta:
        model = HotelReview
        fields = ('rate', 'service', 'reviewer')
