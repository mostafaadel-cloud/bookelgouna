from django.core import validators
from extra_views import InlineFormSet
from image_cropping import ImageCropWidget

from django import forms
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

from booking.models import CartItem
from common.form_mixins import FeaturedImageFormMixin, MultipleImagesFormMixin
from common.forms import TranslationsBaseInline, TravelDatesForm, TimeBasedItemDiscountInlineFormSet
from common.models import TempFile

from .models import SportItem, SportComment, Sport, SportImage, SportReview, SportItemImage, SportItemDiscountPrice


class SportImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SportImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = forms.FileInput()

    class Meta:
        model = SportImage
        fields = ('image',)


class SportImageInline(InlineFormSet):
    form_class = SportImageForm
    model = SportImage
    main_model = Sport
    extra = 0

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        super(SportImageInline, self).__init__(self.main_model, request, instance, view_kwargs, view)

    class Meta:
        fields = ('image',)


class SportTranslationsInline(TranslationsBaseInline):
    main_model = Sport

    class Meta:
        fields = ('title', 'long_description')


class SportForm(FeaturedImageFormMixin, MultipleImagesFormMixin, forms.ModelForm):
    image_model = SportImage

    featured_image_pk = forms.IntegerField(label=_('Featured Image'), required=False, min_value=1)
    multiple_image_pk = forms.CharField(required=False, validators=[validators.validate_comma_separated_integer_list])
    error_messages = {
        'no_featured_image': pgettext_lazy('sport error message on business owner page',
                                           'No featured image.')
    }

    class Meta:
        model = Sport
        fields = ('address',)


class SportItemImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SportItemImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = forms.FileInput()

    class Meta:
        model = SportItemImage
        fields = ('image',)


class SportItemImageInline(InlineFormSet):
    form_class = SportItemImageForm
    model = SportItemImage
    main_model = SportItem
    extra = 0

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        super(SportItemImageInline, self).__init__(self.main_model, request, instance, view_kwargs, view)

    class Meta:
        fields = ('image',)


class SportItemDiscountInline(InlineFormSet):
    model = SportItemDiscountPrice
    main_model = SportItem
    formset_class = TimeBasedItemDiscountInlineFormSet
    max_num = 5
    extra = 5

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        super(SportItemDiscountInline, self).__init__(self.main_model, request, instance, view_kwargs, view)

    class Meta:
        fields = ('number_of_days', 'discount_price')


class SportItemTranslationsInline(TranslationsBaseInline):
    main_model = SportItem

    class Meta:
        fields = ('title', 'long_description',)


class SportItemForm(FeaturedImageFormMixin, MultipleImagesFormMixin, forms.ModelForm):
    image_model = SportItemImage

    featured_image_pk = forms.IntegerField(label=_('Featured Image'), required=False, min_value=1)
    multiple_image_pk = forms.CharField(required=False, validators=[validators.validate_comma_separated_integer_list])
    error_messages = {
        'no_featured_image': pgettext_lazy('sport item error message on business owner page',
                                           'No featured image.')
    }

    def hide_discount_prices(self):
        try:
            val = int(self['type'].value())
        except ValueError:
            return False
        else:
            return val == SportItem.ONE_TIME

    class Meta:
        model = SportItem
        fields = ('type', 'number', 'price', 'show_on_site')


class SportGalleryImageCropForm(forms.ModelForm):
    class Meta:
        model = SportImage
        fields = ('image', 'big_crop', 'small_crop')
        widgets = {
            'image': ImageCropWidget,
        }


class SportFeaturedImageCropForm(forms.ModelForm):
    class Meta:
        model = Sport
        fields = ('featured_image', 'big_crop', 'small_crop')
        widgets = {
            'featured_image': ImageCropWidget,
        }


class SportItemImageCropForm(forms.ModelForm):
    class Meta:
        model = SportItem
        fields = ('featured_image', 'crop', 'cart_crop')
        widgets = {
            'featured_image': ImageCropWidget,
        }


class SportItemGalleryImageCropForm(forms.ModelForm):
    class Meta:
        model = SportItemImage
        fields = ('image', 'crop')
        widgets = {
            'image': ImageCropWidget,
        }


class SportSearchForm(forms.Form):
    type = forms.MultipleChoiceField(label=_('Type'), choices=SportItem.TYPES,
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


class SportCommentForm(forms.ModelForm):
    entity_id = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SportCommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SportComment
        fields = ('text',)

    def clean(self):
        entity_id = self.cleaned_data.get('entity_id')
        if entity_id:
            user = self.request.user
            if user.is_authenticated() and user.is_end_user():
                try:
                    Sport.originals.get(id=entity_id)
                except Sport.DoesNotExist:
                    raise forms.ValidationError(_('No sport with this pk.'))
                if user.sport_comments.filter(entity_id=entity_id).exists():
                    raise forms.ValidationError(_('You have added comment earlier. It might not have been approved yet.'))
            else:
                raise forms.ValidationError(_('Only authorized clients can add new comments.'))


class SportReviewForm(forms.ModelForm):
    class Meta:
        model = SportReview
        fields = ('rate', 'service', 'reviewer')
