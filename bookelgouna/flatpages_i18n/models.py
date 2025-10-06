from __future__ import unicode_literals
from ckeditor.fields import RichTextField
from hvad.models import TranslatableModel, TranslatedFields

from django.db import models
from django.contrib.sites.models import Site
from django.core.urlresolvers import get_script_prefix
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import iri_to_uri, python_2_unicode_compatible


@python_2_unicode_compatible
class FlatPage(TranslatableModel):
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    translations = TranslatedFields(
        title=models.CharField(_('title'), max_length=200),
        desc_metatag=models.CharField(_('description metatag'), max_length=160, help_text=_('max length is 160 letters')),
        content=RichTextField(_('content'))
    )
    template_name = models.CharField(_('template name'), max_length=70, blank=True,
        help_text=_("Example: 'flatpages_i18n/contact_page.html'. If this isn't provided, the system will use 'flatpages_i18n/default.html'."))
    registration_required = models.BooleanField(_('registration required'),
        help_text=_("If this is checked, only logged-in users will be able to view the page."),
        default=False)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    is_published = models.BooleanField(_('is published'), default=True)
    sites = models.ManyToManyField(Site)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        verbose_name = _('Flat Page')
        verbose_name_plural = _('Flat Pages')
        ordering = ('order',)

    def __str__(self):
        return "%s -- %s" % (self.url, self.title_trans)

    @property
    def title_trans(self):
        return self.lazy_translation_getter('title')

    @property
    def desc_metatag_trans(self):
        return self.lazy_translation_getter('desc_metatag')

    @property
    def content_trans(self):
        return self.lazy_translation_getter('content')

    def get_absolute_url(self):
        # Handle script prefix manually because we bypass reverse()
        return iri_to_uri(get_script_prefix().rstrip('/') + self.url)
