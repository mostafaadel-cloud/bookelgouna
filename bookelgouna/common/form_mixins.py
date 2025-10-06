from django import forms
from django.core.exceptions import ImproperlyConfigured

from users.models import User

from hotels.models import Hotel, Room
from apartments.models import Apartment
from transport.models import Transport, TransportItem
from sports.models import Sport, SportItem
from excursions.models import Excursion, ExcursionItem
from entertainment.models import Entertainment, EntertainmentItem

from .models import TempFile


MODEL_TO_CROP_FIELDS = {
    Hotel: ['big_crop', 'small_crop'],
    Room: ['crop'],
    Apartment: ['big_crop', 'small_crop', 'cart_crop'],
    Transport: ['big_crop', 'small_crop'],
    TransportItem: ['crop', 'cart_crop'],
    Sport: ['big_crop', 'small_crop'],
    SportItem: ['crop', 'cart_crop'],
    Excursion: ['big_crop', 'small_crop'],
    ExcursionItem: ['crop', 'cart_crop'],
    Entertainment: ['big_crop', 'small_crop'],
    EntertainmentItem: ['crop', 'cart_crop'],
}


class FeaturedImageFormMixin(object):
    def __init__(self, *args, **kwargs):
        super(FeaturedImageFormMixin, self).__init__(*args, **kwargs)
        if 'featured_image_pk' not in self.fields:
            raise ImproperlyConfigured('Mixin user must define featured_image_pk field.')
        if not hasattr(self, 'error_messages') or 'no_featured_image' not in self.error_messages:
            raise ImproperlyConfigured('Mixin user must define error_messages field with "no_featured_image" message.')

    def clean_featured_image_pk(self):
        featured_image_pk = self.cleaned_data.get('featured_image_pk')
        if featured_image_pk:
            try:
                TempFile.objects.get(pk=featured_image_pk)
            except TempFile.DoesNotExist:
                raise forms.ValidationError(self.error_messages['no_featured_image'], code='no_featured_image')
        return featured_image_pk

    def clean(self):
        super(FeaturedImageFormMixin, self).clean()
        featured_image_pk = self.cleaned_data.get('featured_image_pk')
        # two erroneous situations:
        # 1. instance without featured_image and with empty pk field
        # 2. no instance and empty pk field
        if (self.instance.pk and not self.instance.featured_image and not featured_image_pk) or \
                (not self.instance.pk and not featured_image_pk):
            self.add_error('featured_image_pk', forms.ValidationError(self.error_messages['no_featured_image'],
                                                                      code='no_featured_image'))

    def save_featured_image(self, commit=True, create_view=False):
        """
        :return: true if featured image was changed
        """
        featured_image_pk = self.cleaned_data.get('featured_image_pk')
        if featured_image_pk:
            temp_file = TempFile.objects.get(pk=featured_image_pk)
            inst = self.instance
            inst.featured_image = temp_file.image
            # clear crop fields to recrop newly added image
            if not create_view:
                crop_fields = MODEL_TO_CROP_FIELDS.get(type(self.instance), [])
                for crop_field in crop_fields:
                    setattr(inst, crop_field, None)
            if commit:
                inst.save()
            temp_file.delete()
            return True
        return False


class MultipleImagesFormMixin(object):
    image_model = None

    def __init__(self, *args, **kwargs):
        super(MultipleImagesFormMixin, self).__init__(*args, **kwargs)
        if 'multiple_image_pk' not in self.fields:
            raise ImproperlyConfigured('Mixin user must define multiple_image_pk field.')
        if not hasattr(self, 'image_model') or self.image_model is None:
            raise ImproperlyConfigured('Mixin user must define image_model field.')

    def save_multiple_images(self):
        """
        :return: true if at least one multiple image was added
        """
        multiple_image_pk = self.cleaned_data.get('multiple_image_pk')
        if multiple_image_pk:
            temp_files = TempFile.objects.in_bulk(multiple_image_pk.split(','))
            objs = []
            for pk, temp_file in temp_files.items():
                objs.append(self.image_model(image=temp_file.image, service=self.instance))
                temp_file.delete()
            if objs:
                self.image_model.objects.bulk_create(objs)
                return True
        return False


class PhoneUniquenessMixin(object):

    def __init__(self, *args, **kwargs):
        super(PhoneUniquenessMixin, self).__init__(*args, **kwargs)
        if 'phone' not in self.fields:
            raise ImproperlyConfigured('Mixin user must define phone field.')
        if not hasattr(self, 'error_messages') or 'phone_not_unique' not in self.error_messages:
            raise ImproperlyConfigured('Mixin user must define error_messages field with "phone_not_unique" message.')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            q = User.objects.filter(phone=phone)
            if hasattr(self, 'instance') and self.instance.pk:
                q = q.exclude(pk=self.instance.pk)
            if q.exists():
                raise forms.ValidationError(self.error_messages['phone_not_unique'], code='phone_not_unique')
        return phone
