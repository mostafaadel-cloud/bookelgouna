# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings, Client

from users.tests.factories import create_apt_business_owner

from ..models import Apartment, ApartmentImage


@override_settings(MEDIA_ROOT=os.path.join(settings.BASE_DIR, 'testdata/media/'))
class ApartmentModerationTestCase(TestCase):

    def setUp(self):
        self.owner = create_apt_business_owner()
        o = Apartment()
        o.owner = self.owner
        o.address = "Baker St. 221B"
        o.featured_image = '1.jpg'
        o.save()
        o.images.create(image='2.jpg')
        o.translate('en')
        o.title = 'Apartment #1'
        o.long_description = 'Apartment company #1'
        o.slug = o.generate_slug(commit=True)

    def test_duplicate_creation(self):
        o = Apartment.objects.first()
        original_pk_before_dup = o.pk
        d = o.create_object_duplicate_from_given()
        d = Apartment.objects.get(pk=d.pk)  # refresh it from db
        self.assertEqual(original_pk_before_dup, o.pk)
        self.assertNotEqual(original_pk_before_dup, d.pk)
        # 1: check whether flat data was duplicated correctly
        self.assertEqual(d.owner, self.owner)
        self.assertEqual(d.address, "Baker St. 221B")
        self.assertEqual(d.featured_image, "1.jpg")
        self.assertEqual(d.images.first().image, "2.jpg")
        # 2: check whether original flat data has not been corrupted
        self.assertEqual(o.owner, self.owner)
        self.assertEqual(o.address, "Baker St. 221B")
        self.assertEqual(o.featured_image, "1.jpg")
        self.assertEqual(o.images.first().image, "2.jpg")
        # 3: check related objects of duplicate and original Apartment
        # 3.1: translations
        d_trans = Apartment.objects.language('en').get(pk=d.pk)
        self.assertEqual(d_trans.language_code, 'en')
        self.assertEqual(d_trans.title, 'Apartment #1')
        self.assertEqual(d_trans.long_description, 'Apartment company #1')
        o_trans = Apartment.objects.language('en').get(pk=o.pk)
        self.assertEqual(o_trans.language_code, 'en')
        self.assertEqual(o_trans.title, 'Apartment #1')
        self.assertEqual(o_trans.long_description, 'Apartment company #1')
        self.assertEqual(o.translations.count(), d.translations.count())
        original_trans_pks = sorted([trans.pk for trans in o.translations.all()])
        duplicate_trans_pks = sorted([trans.pk for trans in d.translations.all()])
        self.assertNotEquals(original_trans_pks, duplicate_trans_pks)
        # 3.2: images
        self.assertEqual(d.images.first().image, '2.jpg')
        self.assertEqual(o.images.first().image, '2.jpg')
        self.assertEqual(o.images.count(), d.images.count())
        original_images_pks = sorted([img_obj.pk for img_obj in o.images.all()])
        duplicate_images_pks = sorted([img_obj.pk for img_obj in d.images.all()])
        self.assertNotEquals(original_images_pks, duplicate_images_pks)
        # 4: slugs should be different and not null
        self.assertNotEqual(o.slug, '')
        self.assertNotEqual(d.slug, '')
        self.assertNotEqual(o.slug, d.slug)

    def test_moderation_and_approving(self):
        o = Apartment.objects.first()
        d = o.create_object_duplicate_from_given()
        old_dup_pk = d.pk
        Apartment.rewrite_origin_object_with_approved_duplicate(d.origin, d)
        self.assertRaises(Apartment.DoesNotExist, Apartment.objects.get, pk=old_dup_pk)  # old duplicate does not exist
        # there is no related objects of duplicate anymore
        dup_images = ApartmentImage.objects.filter(service_id=old_dup_pk)
        self.assertFalse(dup_images.exists())

    def test_show_on_site_change_view_not_trigger_moderation_status(self):
        o = Apartment.objects.first()
        d = o.create_object_duplicate_from_given()
        client = Client()
        client.login(username=self.owner.username, password='1234')
        # imitate previous approval (original is approved and duplicate is in intermediate updating state)
        o.status = Apartment.APPROVED
        o.save()
        d.status = Apartment.UPDATING
        d.save()
        # set show_on_site=False (send empty POST data)
        resp = client.post(reverse('apt_show_on_site_attr_change', args=(d.slug,)),
                           data={})
        self.assertEqual(resp.status_code, 200)
        # refetch
        o = Apartment.objects.get(pk=o.pk)
        d = Apartment.objects.get(pk=d.pk)
        self.assertFalse(o.show_on_site)
        self.assertFalse(d.show_on_site)
        self.assertEqual(o.status, Apartment.APPROVED)
        self.assertEqual(d.status, Apartment.UPDATING)
        # set show_on_site=True
        resp = client.post(reverse('apt_show_on_site_attr_change', args=(d.slug,)),
                           data={'enable': ''})
        self.assertEqual(resp.status_code, 200)
        # refetch
        o = Apartment.objects.get(pk=o.pk)
        d = Apartment.objects.get(pk=d.pk)
        self.assertTrue(o.show_on_site)
        self.assertTrue(d.show_on_site)
        self.assertEqual(o.status, Apartment.APPROVED)
        self.assertEqual(d.status, Apartment.UPDATING)

