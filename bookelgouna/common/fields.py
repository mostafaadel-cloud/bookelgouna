from django import forms
from skd_tools.fields import TypedFileField

from django.utils.translation import ugettext_lazy as _


class TypedImageField(TypedFileField):
    default_error_messages = {
        'invalid_format': _("Wrong file format."),
        'invalid_size': _("This file is too big (max size is %(size)d MB).")
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('allowed_mimes', ['image/png', 'image/jpeg', 'image/pjpeg'])
        kwargs.setdefault('allowed_exts', ['jpeg', 'jpg', 'png'])
        kwargs.setdefault('max_size', 10)
        super(TypedImageField, self).__init__(*args, **kwargs)
