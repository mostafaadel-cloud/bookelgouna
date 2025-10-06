# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from extra_views import InlineFormSet
from image_cropping import ImageCropWidget

from django import forms
from django.core import validators
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

from booking.models import CartItem
from common.forms import TranslationsBaseInline, TravelDatesForm, TimeBasedItemDiscountInlineFormSet
from common.form_mixins import FeaturedImageFormMixin, MultipleImagesFormMixin

from .models import TransportItem, TransportComment, Transport, TransportImage, TransportReview, TransportItemImage, \
    TransportItemDiscountPrice


class TransportImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TransportImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = forms.FileInput()

    class Meta:
        model = TransportImage
        fields = ('image',)


class TransportImageInline(InlineFormSet):
    form_class = TransportImageForm
    model = TransportImage
    main_model = Transport
    extra = 0

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        super(TransportImageInline, self).__init__(self.main_model, request, instance, view_kwargs, view)

    class Meta:
        fields = ('image',)


class TransportTranslationsInline(TranslationsBaseInline):
    main_model = Transport

    class Meta:
        fields = ('title', 'long_description')


class TransportForm(FeaturedImageFormMixin, MultipleImagesFormMixin, forms.ModelForm):
    image_model = TransportImage

    featured_image_pk = forms.IntegerField(label=_('Featured Image'), required=False, min_value=1)
    multiple_image_pk = forms.CharField(required=False, validators=[validators.validate_comma_separated_integer_list])
    error_messages = {
        'no_featured_image': pgettext_lazy('transport error message on business owner page',
                                           'No featured image.')
    }

    class Meta:
        model = Transport
        fields = ('address',)


class TransportItemImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TransportItemImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = forms.FileInput()

    class Meta:
        model = TransportItemImage
        fields = ('image',)


class TransportItemImageInline(InlineFormSet):
    form_class = TransportItemImageForm
    model = TransportItemImage
    main_model = TransportItem
    extra = 0

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        super(TransportItemImageInline, self).__init__(self.main_model, request, instance, view_kwargs, view)

    class Meta:
        fields = ('image',)


class TransportItemDiscountInline(InlineFormSet):
    model = TransportItemDiscountPrice
    main_model = TransportItem
    formset_class = TimeBasedItemDiscountInlineFormSet
    max_num = 5
    extra = 5

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        super(TransportItemDiscountInline, self).__init__(self.main_model, request, instance, view_kwargs, view)

    class Meta:
        fields = ('number_of_days', 'discount_price')


class TransportItemTranslationsInline(TranslationsBaseInline):
    main_model = TransportItem

    class Meta:
        fields = ('title', 'long_description',)


class TransportItemForm(FeaturedImageFormMixin, MultipleImagesFormMixin, forms.ModelForm):
    image_model = TransportItemImage

    featured_image_pk = forms.IntegerField(label=_('Featured Image'), required=False, min_value=1)
    multiple_image_pk = forms.CharField(required=False, validators=[validators.validate_comma_separated_integer_list])
    error_messages = {
        'no_featured_image': pgettext_lazy('transport item error message on business owner page',
                                           'No featured image.')
    }

    def hide_discount_prices(self):
        try:
            val = int(self['type'].value())
        except ValueError:
            return False
        else:
            return val == TransportItem.ONE_RIDE

    class Meta:
        model = TransportItem
        fields = ('type', 'number', 'price', 'show_on_site')


class TransportGalleryImageCropForm(forms.ModelForm):
    class Meta:
        model = TransportImage
        fields = ('image', 'big_crop', 'small_crop')
        widgets = {
            'image': ImageCropWidget,
        }


class TransportFeaturedImageCropForm(forms.ModelForm):
    class Meta:
        model = Transport
        fields = ('featured_image', 'big_crop', 'small_crop')
        widgets = {
            'featured_image': ImageCropWidget,
        }


class TransportItemImageCropForm(forms.ModelForm):
    class Meta:
        model = TransportItem
        fields = ('featured_image', 'crop', 'cart_crop')
        widgets = {
            'featured_image': ImageCropWidget,
        }


class TransportItemGalleryImageCropForm(forms.ModelForm):
    class Meta:
        model = TransportItemImage
        fields = ('image', 'crop')
        widgets = {
            'image': ImageCropWidget,
        }


class TransportSearchForm(forms.Form):
    type = forms.MultipleChoiceField(label=_('Type'), choices=TransportItem.TYPES,
                                     widget=forms.CheckboxSelectMultiple)
    from_price = forms.IntegerField(widget=forms.HiddenInput)
    to_price = forms.IntegerField(widget=forms.HiddenInput)
    page = forms.IntegerField(widget=forms.HiddenInput, initial=1)


class ItemSearchForm(TravelDatesForm):
    pass


class CartItemForm(forms.ModelForm):
    from_date = forms.DateField(input_formats=['%d.%m.%Y'], widget=forms.DateInput(format='%d.%m.%Y'), required=False)
    to_date = forms.DateField(input_formats=['%d.%m.%Y'], widget=forms.DateInput(format='%d.%m.%Y'), required=False)

    class Meta:
        model = CartItem
        fields = ('from_date', 'to_date')


class TransportCommentForm(forms.ModelForm):
    entity_id = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TransportCommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = TransportComment
        fields = ('text',)

    def clean(self):
        entity_id = self.cleaned_data.get('entity_id')
        if entity_id:
            user = self.request.user
            if user.is_authenticated() and user.is_end_user():
                try:
                    Transport.originals.get(id=entity_id)
                except Transport.DoesNotExist:
                    raise forms.ValidationError(_('No transport with this pk.'))
                if user.transport_comments.filter(entity_id=entity_id).exists():
                    raise forms.ValidationError(_('You have added comment earlier. It might not have been approved yet.'))
            else:
                raise forms.ValidationError(_('Only authorized clients can add new comments.'))


class TransportReviewForm(forms.ModelForm):
    class Meta:
        model = TransportReview
        fields = ('rate', 'service', 'reviewer')
