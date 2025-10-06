# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from itertools import chain
from django import forms
from django.db.models import Prefetch
from django.forms.utils import flatatt
from django.forms.widgets import SubWidget
from django.utils.encoding import force_unicode, python_2_unicode_compatible
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from .models import HotelAmenityCategory, HotelAmenity


class CheckboxInputIter(SubWidget):
    """
    An object used by CheckboxRenderer that represents a single
    <input type='checkbox'>.
    """
    def __init__(self, name, value, attrs, choice, index):
        self.name, self.value = name, value
        self.attrs = attrs

        self.choice_value = force_unicode(choice[0])
        self.choice_label = force_unicode(choice[1])

        self.attrs.update({'cat_name': choice[2]})

        self.index = index

    def __unicode__(self):
        return self.render()

    def __str__(self):
        args = [self.name, self.value, self.attrs]
        if self.choices:
            args.append(self.choices)
        return self.render(*args)

    # def __str__(self):
    #     return self.render()

    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs

        if 'id' in self.attrs:
            label_for = ' class="select-amenities__checkbox-label" for="%s_%s"' % (self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = conditional_escape(force_unicode(self.choice_label))
        return mark_safe(u'%s<label%s>%s</label>' % (self.tag(), label_for, choice_label))

    def is_checked(self):
        return self.choice_value in self.value

    def tag(self):
        if 'id' in self.attrs:
            self.attrs['id'] = '%s_%s' % (self.attrs['id'], self.index)
        final_attrs = dict(self.attrs, type='checkbox', name=self.name, value=self.choice_value)
        if self.is_checked():
            final_attrs['checked'] = 'checked'
        return mark_safe(u'<input display="none" class="select-amenities__checkbox-input" %s />' % flatatt(final_attrs))


@python_2_unicode_compatible
class CheckboxRenderer(object):
    def __init__(self, name, value, attrs, choices):
        self.name, self.value, self.attrs = name, value, attrs
        self.choices = choices

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield CheckboxInputIter(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx]  # Let the IndexError propogate
        return CheckboxInputIter(self.name, self.value, self.attrs.copy(), choice, idx)

    def __unicode__(self):
        return self.render()

    def __str__(self):
        return self.render()

    def render(self):
        """Outputs a <ul> for this set of checkbox fields."""
        return mark_safe(u'<ul>\n%s\n</ul>' % u'\n'.join([u'<li>%s</li>' % force_unicode(w) for w in self]))


class CheckboxSelectMultipleIter(forms.CheckboxSelectMultiple):
    """
    Checkbox multi select field that enables iteration of each checkbox
    Similar to django.forms.widgets.RadioSelect
    """
    renderer = CheckboxRenderer

    def __init__(self, *args, **kwargs):
        # Override the default renderer if we were passed one.
        renderer = kwargs.pop('renderer', None)
        if renderer:
            self.renderer = renderer
        super(CheckboxSelectMultipleIter, self).__init__(*args, **kwargs)

    def subwidgets(self, name, value, attrs=None, choices=()):
        for widget in self.get_renderer(name, value, attrs, choices):
            yield widget

    def get_renderer(self, name, value, attrs=None, choices=()):
        """Returns an instance of the renderer."""
        choices_ = [(n.id, n.name, n.category.name) for n in HotelAmenity.objects.language().fallbacks().prefetch_related('translations').prefetch_related(Prefetch('category', queryset=HotelAmenityCategory.objects.language().fallbacks()))]
        # choices_ = [ast.literal_eval(i[1]).iteritems() for i in self.choices]
        # choices_ = [(a[1], b[1], c[1]) for a, b, c in choices_]

        if value is None: value = ''
        str_values = set([force_unicode(v) for v in value]) # Normalize to string.
        if attrs is None:
            attrs = {}
        if 'id' not in attrs:
            attrs['id'] = name
        final_attrs = self.build_attrs(attrs)
        choices = list(chain(choices_, choices))
        return self.renderer(name, str_values, final_attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        return self.get_renderer(name, value, attrs, choices).render()

    def id_for_label(self, id_):
        if id_:
            id_ += '_0'
        return id_


class RoomCheckboxSelectMultipleIter(forms.CheckboxSelectMultiple):
    """
    Checkbox multi select field that enables iteration of each checkbox
    Similar to django.forms.widgets.RadioSelect
    """
    renderer = CheckboxRenderer

    def __init__(self, *args, **kwargs):
        # Override the default renderer if we were passed one.
        renderer = kwargs.pop('renderer', None)
        if renderer:
            self.renderer = renderer
        super(RoomCheckboxSelectMultipleIter, self).__init__(*args, **kwargs)

    def subwidgets(self, name, value, attrs=None, choices=()):
        for widget in self.get_renderer(name, value, attrs, choices):
            yield widget

    def get_renderer(self, name, value, attrs=None, choices=()):
        """Returns an instance of the renderer."""
        choices_ = [(n.id, n.name, n.category.name) for n in HotelAmenity.objects.language().fallbacks().prefetch_related('translations').prefetch_related(Prefetch('category', queryset=HotelAmenityCategory.objects.language().fallbacks()))]
        # choices_ = [ast.literal_eval(i[1]).iteritems() for i in self.choices]
        # choices_ = [(a[1], b[1], c[1]) for a, b, c in choices_]

        if value is None: value = ''
        str_values = set([force_unicode(v) for v in value]) # Normalize to string.
        if attrs is None:
            attrs = {}
        if 'id' not in attrs:
            attrs['id'] = name
        final_attrs = self.build_attrs(attrs)
        choices = list(chain(choices_, choices))
        return self.renderer(name, str_values, final_attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        return self.get_renderer(name, value, attrs, choices).render()

    def id_for_label(self, id_):
        if id_:
            id_ += '_0'
        return id_
