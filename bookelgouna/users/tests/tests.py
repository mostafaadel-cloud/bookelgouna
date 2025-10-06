from django.core.urlresolvers import reverse
from django.shortcuts import resolve_url
from django.test import TestCase, Client

from hotels.models import Hotel

from .factories import create_end_user, create_hotel_business_owner
from ..exceptions import BusinessOwnerOnly
from ..models import BusinessOwnerInfo


class EndUserTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.end_user = create_end_user()

    def test_service_type_related_methods(self):
        self.assertRaises(BusinessOwnerOnly, getattr, self.end_user, 'service_type')
        self.assertRaises(BusinessOwnerOnly, self.end_user.get_service_type_full_name)
        self.assertRaises(BusinessOwnerOnly, getattr, self.end_user, 'services_manager')
        self.assertRaises(BusinessOwnerOnly, self.end_user.get_original_service)
        self.assertRaises(BusinessOwnerOnly, self.end_user.has_service)

    def test_authorization_of_end_user_via_correct_login(self):
        client = Client()
        resp = client.post(reverse('account_login'),
                           data={
                               'login': self.end_user.username,
                               'password': '1234'
                           }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, reverse('user_profile'))

    def test_authorization_of_end_user_via_incorrect_login(self):
        client = Client()
        resp = client.post(reverse('business_login'),
                           data={
                               'login': self.end_user.username,
                               'password': '1234'
                           })
        self.assertRedirects(resp, resolve_url('account_login'))


class BusinessOwnerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.owner = create_hotel_business_owner()

    def test_authorization_of_business_owner_via_correct_login(self):
        client = Client()
        resp = client.post(reverse('business_login'),
                           data={
                               'login': self.owner.username,
                               'password': '1234'
                           }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, reverse('business_profile'))

    def test_authorization_of_business_owner_via_incorrect_login(self):
        client = Client()
        resp = client.post(reverse('account_login'),
                           data={
                               'login': self.owner.username,
                               'password': '1234'
                           })
        self.assertRedirects(resp, resolve_url('business'))

    def test_service_type_related_methods(self):
        self.assertEqual(self.owner.service_type, BusinessOwnerInfo.HOTEL)
        self.assertEqual(self.owner.get_service_type_full_name(),
                         BusinessOwnerInfo.SERVICE_TYPES[BusinessOwnerInfo.HOTEL][1])
        self.assertEqual(self.owner.services_manager.model, Hotel)
        self.assertFalse(self.owner.has_service())
        self.assertRaises(Hotel.DoesNotExist, self.owner.get_original_service)
