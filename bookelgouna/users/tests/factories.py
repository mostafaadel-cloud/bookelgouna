from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers import registry
from allauth.socialaccount.providers.facebook.provider import FacebookProvider
from django.contrib.sites.models import Site
import factory

from ..models import User, BusinessOwnerInfo


class EndUserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'enduser%d' % n)
    email = factory.Sequence(lambda n: 'enduser%d@bookelgouna.com' % n)
    first_name = factory.Sequence(lambda n: 'enduser%d first name' % n)
    last_name = factory.Sequence(lambda n: 'enduser%d last name' % n)
    password = factory.PostGenerationMethodCall('set_password', '1234')
    is_superuser = False
    is_active = True

    class Meta:
        model = User


def init_socialapp():
    # it is required to get allauth login functionality work
    if not SocialApp.objects.exists():
        provider = registry.by_id(FacebookProvider.id)
        app = SocialApp.objects.create(provider=provider.id,
                                       name=provider.id,
                                       client_id='app123id',
                                       key=provider.id,
                                       secret='dummy')
        app.sites.add(Site.objects.get_current())


def create_end_user():
    init_socialapp()
    enduser = EndUserFactory()
    EmailAddress.objects.create(user=enduser, email=enduser.email, verified=True, primary=True)
    return enduser


class BusinessOwnerFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'businessowner%d' % n)
    email = factory.Sequence(lambda n: 'businessowner%d@bookelgouna.com' % n)
    first_name = factory.Sequence(lambda n: 'businessowner%d first name' % n)
    last_name = factory.Sequence(lambda n: 'businessowner%d last name' % n)
    type = User.BUSINESS_OWNER
    password = factory.PostGenerationMethodCall('set_password', '1234')
    is_superuser = False
    is_active = True

    class Meta:
        model = User


def create_business_owner_with_type(service_type):
    init_socialapp()
    business_owner = BusinessOwnerFactory()
    EmailAddress.objects.create(user=business_owner, email=business_owner.email, verified=True, primary=True)
    BusinessOwnerInfo.objects.create(user=business_owner, service_type=service_type)
    return business_owner


def create_hotel_business_owner():
    return create_business_owner_with_type(BusinessOwnerInfo.HOTEL)


def create_apt_business_owner():
    return create_business_owner_with_type(BusinessOwnerInfo.APARTMENT)


def create_transport_business_owner():
    return create_business_owner_with_type(BusinessOwnerInfo.TRANSPORT)


def create_excursion_business_owner():
    return create_business_owner_with_type(BusinessOwnerInfo.EXCURSION)


def create_sport_business_owner():
    return create_business_owner_with_type(BusinessOwnerInfo.SPORT)


def create_things_to_do_business_owner():
    return create_business_owner_with_type(BusinessOwnerInfo.ENTERTAINMENT)
