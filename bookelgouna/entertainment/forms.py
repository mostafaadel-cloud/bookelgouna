from django.core import validators
from extra_views import InlineFormSet
from image_cropping import ImageCropWidget

from django import forms
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

from booking.models import CartItem
from common.form_mixins import FeaturedImageFormMixin, MultipleImagesFormMixin
from common.forms import TranslationsBaseInline, TravelDatesForm, TimeBasedItemDiscountInlineFormSet
from common.models import TempFile

from .models import EntertainmentItem, EntertainmentComment, Entertainment, EntertainmentImage, EntertainmentReview,\
    EntertainmentItemImage, EntertainmentItemDiscountPrice


class EntertainmentImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EntertainmentImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = forms.FileInput()

    class Meta:
        model = EntertainmentImage
        fields = ('image',)


class EntertainmentImageInline(InlineFormSet):
    form_class = EntertainmentImageForm
    model = EntertainmentImage
    main_model = Entertainment
    extra = 0

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        super(EntertainmentImageInline, self).__init__(self.main_model, request, instance, view_kwargs, view)

    class Meta:
        fields = ('image',)


class EntertainmentTranslationsInline(TranslationsBaseInline):
    main_model = Entertainment

    class Meta:
        fields = ('title', 'long_description')


class EntertainmentForm(FeaturedImageFormMixin, MultipleImagesFormMixin, forms.ModelForm):
    image_model = EntertainmentImage

    featured_image_pk = forms.IntegerField(label=_('Featured Image'), required=False, min_value=1)
    multiple_image_pk = forms.CharField(required=False, validators=[validators.validate_comma_separated_integer_list])
    error_messages = {
        'no_featured_image': pgettext_lazy('entertainment error message on business owner page',
                                           'No featured image.')
    }

    class Meta:
        model = Entertainment
        fields = ('address',)


class EntertainmentItemImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EntertainmentItemImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = forms.FileInput()

    class Meta:
        model = EntertainmentItemImage
        fields = ('image',)


class EntertainmentItemImageInline(InlineFormSet):
    form_class = EntertainmentItemImageForm
    model = EntertainmentItemImage
    main_model = EntertainmentItem
    extra = 0

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        super(EntertainmentItemImageInline, self).__init__(self.main_model, request, instance, view_kwargs, view)

    class Meta:
        fields = ('image',)


class EntertainmentItemDiscountInline(InlineFormSet):
    model = EntertainmentItemDiscountPrice
    main_model = EntertainmentItem
    formset_class = TimeBasedItemDiscountInlineFormSet
    max_num = 5
    extra = 5

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        super(EntertainmentItemDiscountInline, self).__init__(self.main_model, request, instance, view_kwargs, view)

    class Meta:
        fields = ('number_of_days', 'discount_price')


class EntertainmentItemTranslationsInline(TranslationsBaseInline):
    main_model = EntertainmentItem

    class Meta:
        fields = ('title', 'long_description',)


class EntertainmentItemForm(FeaturedImageFormMixin, MultipleImagesFormMixin, forms.ModelForm):
    image_model = EntertainmentItemImage

    featured_image_pk = forms.IntegerField(label=_('Featured Image'), required=False, min_value=1)
    multiple_image_pk = forms.CharField(required=False, validators=[validators.validate_comma_separated_integer_list])
    error_messages = {
        'no_featured_image': pgettext_lazy('entertainment item error message on business owner page',
                                           'No featured image.')
    }

    def hide_discount_prices(self):
        try:
            val = int(self['type'].value())
        except ValueError:
            return False
        else:
            return val == EntertainmentItem.ONE_TIME

    class Meta:
        model = EntertainmentItem
        fields = ('type', 'number', 'price', 'show_on_site')


class EntertainmentGalleryImageCropForm(forms.ModelForm):
    class Meta:
        model = EntertainmentImage
        fields = ('image', 'big_crop', 'small_crop')
        widgets = {
            'image': ImageCropWidget,
        }


class EntertainmentFeaturedImageCropForm(forms.ModelForm):
    class Meta:
        model = Entertainment
        fields = ('featured_image', 'big_crop', 'small_crop')
        widgets = {
            'featured_image': ImageCropWidget,
        }


class EntertainmentItemImageCropForm(forms.ModelForm):
    class Meta:
        model = EntertainmentItem
        fields = ('featured_image', 'crop', 'cart_crop')
        widgets = {
            'featured_image': ImageCropWidget,
        }


class EntertainmentItemGalleryImageCropForm(forms.ModelForm):
    class Meta:
        model = EntertainmentItemImage
        fields = ('image', 'crop')
        widgets = {
            'image': ImageCropWidget,
        }


class EntertainmentSearchForm(forms.Form):
    type = forms.MultipleChoiceField(label=_('Type'), choices=EntertainmentItem.TYPES,
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


class EntertainmentCommentForm(forms.ModelForm):
    entity_id = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EntertainmentCommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = EntertainmentComment
        fields = ('text',)

    def clean(self):
        entity_id = self.cleaned_data.get('entity_id')
        if entity_id:
            user = self.request.user
            if user.is_authenticated() and user.is_end_user():
                try:
                    Entertainment.originals.get(id=entity_id)
                except Entertainment.DoesNotExist:
                    raise forms.ValidationError(_('No entertainment with this pk.'))
                if user.entertainment_comments.filter(entity_id=entity_id).exists():
                    raise forms.ValidationError(_('You have added comment earlier. It might not have been approved yet.'))
            else:
                raise forms.ValidationError(_('Only authorized clients can add new comments.'))


class EntertainmentReviewForm(forms.ModelForm):
    class Meta:
        model = EntertainmentReview
        fields = ('rate', 'service', 'reviewer')
