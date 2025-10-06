from django.core import validators
from extra_views import InlineFormSet
from image_cropping import ImageCropWidget

from django import forms
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

from booking.models import CartItem
from common.forms import TranslationsBaseInline, TravelDatesForm, TimeBasedItemDiscountInlineFormSet
from common.form_mixins import FeaturedImageFormMixin, MultipleImagesFormMixin

from .models import ExcursionItem, ExcursionComment, Excursion, ExcursionImage, ExcursionReview, ExcursionItemImage, \
    ExcursionItemDiscountPrice


class ExcursionImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ExcursionImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = forms.FileInput()

    class Meta:
        model = ExcursionImage
        fields = ('image',)


class ExcursionImageInline(InlineFormSet):
    form_class = ExcursionImageForm
    model = ExcursionImage
    main_model = Excursion
    extra = 0

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        super(ExcursionImageInline, self).__init__(self.main_model, request, instance, view_kwargs, view)

    class Meta:
        fields = ('image',)


class ExcursionTranslationsInline(TranslationsBaseInline):
    main_model = Excursion

    class Meta:
        fields = ('title', 'long_description')


class ExcursionForm(FeaturedImageFormMixin, MultipleImagesFormMixin, forms.ModelForm):
    image_model = ExcursionImage

    featured_image_pk = forms.IntegerField(label=_('Featured Image'), required=False, min_value=1)
    multiple_image_pk = forms.CharField(required=False, validators=[validators.validate_comma_separated_integer_list])
    error_messages = {
        'no_featured_image': pgettext_lazy('excursion error message on business owner page',
                                           'No featured image.')
    }

    class Meta:
        model = Excursion
        fields = ('address',)


class ExcursionItemImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ExcursionItemImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = forms.FileInput()

    class Meta:
        model = ExcursionItemImage
        fields = ('image',)


class ExcursionItemImageInline(InlineFormSet):
    form_class = ExcursionItemImageForm
    model = ExcursionItemImage
    main_model = ExcursionItem
    extra = 0

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        super(ExcursionItemImageInline, self).__init__(self.main_model, request, instance, view_kwargs, view)

    class Meta:
        fields = ('image',)


class ExcursionItemDiscountInline(InlineFormSet):
    model = ExcursionItemDiscountPrice
    main_model = ExcursionItem
    formset_class = TimeBasedItemDiscountInlineFormSet
    max_num = 5
    extra = 5

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        super(ExcursionItemDiscountInline, self).__init__(self.main_model, request, instance, view_kwargs, view)

    class Meta:
        fields = ('number_of_days', 'discount_price')



class ExcursionItemTranslationsInline(TranslationsBaseInline):
    main_model = ExcursionItem

    class Meta:
        fields = ('title', 'long_description',)


class ExcursionItemForm(FeaturedImageFormMixin, MultipleImagesFormMixin, forms.ModelForm):
    image_model = ExcursionItemImage

    featured_image_pk = forms.IntegerField(label=_('Featured Image'), required=False, min_value=1)
    multiple_image_pk = forms.CharField(required=False, validators=[validators.validate_comma_separated_integer_list])
    error_messages = {
        'no_featured_image': pgettext_lazy('excursion item error message on business owner page',
                                           'No featured image.')
    }

    def hide_discount_prices(self):
        try:
            val = int(self['type'].value())
        except ValueError:
            return False
        else:
            return val == ExcursionItem.ONE_TIME

    class Meta:
        model = ExcursionItem
        fields = ('type', 'number', 'price', 'show_on_site')


class ExcursionGalleryImageCropForm(forms.ModelForm):
    class Meta:
        model = ExcursionImage
        fields = ('image', 'big_crop', 'small_crop')
        widgets = {
            'image': ImageCropWidget,
        }


class ExcursionFeaturedImageCropForm(forms.ModelForm):
    class Meta:
        model = Excursion
        fields = ('featured_image', 'big_crop', 'small_crop')
        widgets = {
            'featured_image': ImageCropWidget,
        }


class ExcursionItemImageCropForm(forms.ModelForm):
    class Meta:
        model = ExcursionItem
        fields = ('featured_image', 'crop', 'cart_crop')
        widgets = {
            'featured_image': ImageCropWidget,
        }


class ExcursionItemGalleryImageCropForm(forms.ModelForm):
    class Meta:
        model = ExcursionItemImage
        fields = ('image', 'crop')
        widgets = {
            'image': ImageCropWidget,
        }


class ExcursionSearchForm(forms.Form):
    type = forms.MultipleChoiceField(label=_('Type'), choices=ExcursionItem.TYPES,
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


class ExcursionCommentForm(forms.ModelForm):
    entity_id = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ExcursionCommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ExcursionComment
        fields = ('text',)

    def clean(self):
        entity_id = self.cleaned_data.get('entity_id')
        if entity_id:
            user = self.request.user
            if user.is_authenticated() and user.is_end_user():
                try:
                    Excursion.originals.get(id=entity_id)
                except Excursion.DoesNotExist:
                    raise forms.ValidationError(_('No excursion with this pk.'))
                if user.excursion_comments.filter(entity_id=entity_id).exists():
                    raise forms.ValidationError(_('You have added comment earlier. It might not have been approved yet.'))
            else:
                raise forms.ValidationError(_('Only authorized clients can add new comments.'))


class ExcursionReviewForm(forms.ModelForm):
    class Meta:
        model = ExcursionReview
        fields = ('rate', 'service', 'reviewer')
