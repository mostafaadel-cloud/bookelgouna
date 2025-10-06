# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ckeditor.fields import RichTextField
from django.core.urlresolvers import reverse
from django.utils import translation
from django.utils.encoding import force_text
from hvad.manager import TranslationManager
from hvad.models import TranslatableModel, TranslatedFields

from django.core.mail import send_mail
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site
from django.conf import settings


class BookingEmailTemplateManager(TranslationManager):

    DEFAULT_EMAIL_LANGUAGE_CODE = 'en'

    def create_and_send_email_from_template_for_order_item(self, email_type, order_item):

        assert email_type in BookingEmailTemplate.EMAIL_TYPES_INDEXES, \
            'Improperly configured: email type has invalid value.'

        owner = order_item.owner.get_base_account_or_self()
        tourist = order_item.order.user

        email_to_tourist = email_type in self.model.TOURIST_EMAILS
        recipient = tourist if email_to_tourist else owner

        template_translations = self.model.objects.untranslated().get(email_type=email_type).translations.all()
        preferred_language = recipient.preferred_language
        try:
            trans = template_translations.get(language_code=preferred_language)
            used_language = preferred_language
        except BookingEmailTemplate.DoesNotExist:
            used_language = self.DEFAULT_EMAIL_LANGUAGE_CODE
            trans = template_translations.get(language_code=used_language)

        actual_language = translation.get_language()
        revert_language_back = False

        if actual_language != used_language:
            translation.activate(used_language)
            revert_language_back = True

        if email_to_tourist:
            bookings_url = reverse('user_bookings')
        else:
            bookings_url = reverse('business_bookings')

        subject = trans.subject
        subject = subject.replace('[EMAIL]', recipient.email)
        subject = subject.replace('[LOGIN]', recipient.username)
        subject = subject.replace('[FIRST_NAME]', recipient.first_name)
        subject = subject.replace('[LAST_NAME]', recipient.last_name)

        email_body = trans.email_body
        email_body = email_body.replace('[RECIPIENT_EMAIL]', recipient.email)
        email_body = email_body.replace('[RECIPIENT_USERNAME]', recipient.username)
        email_body = email_body.replace('[RECIPIENT_FIRST_NAME]', recipient.first_name)
        email_body = email_body.replace('[RECIPIENT_LAST_NAME]', recipient.last_name)
        email_body = email_body.replace('[ORDER_ITEM_ID]', str(order_item.pk))
        email_body = email_body.replace('[DATES]', force_text(order_item.dates()))
        email_body = email_body.replace('[BOOKINGS_LINK]', ''.join(['http://', Site.objects.get_current().domain,
                                                                    bookings_url]))
        email_body = email_body.replace('[ITEM_DESCRIPTION]', order_item.item_desc)
        email_body = email_body.replace('[QUANTITY]', str(order_item.quantity))
        email_body = email_body.replace('[PRICE]', str(order_item.price))

        if email_to_tourist:
            if email_type == self.model.NOTIFY_TOURIST_ABOUT_BOOKING_APPROVAL:
                email_body = email_body.replace('[OWNER_EMAIL]', order_item.owner_email())
                email_body = email_body.replace('[OWNER_PHONE]', force_text(order_item.owner_phone()))
        else:
            email_body = email_body.replace('[TOURIST_ID]', str(tourist.pk))
            if email_type == self.model.NOTIFY_OWNER_ABOUT_BOOKING_APPROVAL:
                email_body = email_body.replace('[TOURIST_EMAIL]', tourist.email)
                email_body = email_body.replace('[TOURIST_PHONE]', force_text(tourist.phone))
            elif email_type == self.model.NOTIFY_OWNER_ABOUT_BOOKING_AUTO_REJECT:
                email_body = email_body.replace('[HOURS_OF_INACTIVITY]',
                                                str(settings.BOOKING_REJECT_AFTER_HOURS_OF_INACTIVITY))

        if revert_language_back:
            translation.activate(actual_language)

        send_mail(subject=subject, message=email_body, from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[recipient.email], html_message=email_body)

class BookingEmailTemplate(TranslatableModel):

    NOTIFY_OWNER_ABOUT_NEW_BOOKING = 1
    NOTIFY_OWNER_ABOUT_BOOKING_APPROVAL = 2
    NOTIFY_TOURIST_ABOUT_BOOKING_APPROVAL = 3
    NOTIFY_OWNER_ABOUT_BOOKING_MANUAL_REJECT = 4
    NOTIFY_TOURIST_ABOUT_BOOKING_MANUAL_REJECT = 5
    NOTIFY_OWNER_ABOUT_BOOKING_AUTO_REJECT = 6
    NOTIFY_TOURIST_ABOUT_BOOKING_AUTO_REJECT = 7
    NOTIFY_OWNER_ABOUT_NOSHOW_USED = 8
    NOTIFY_TOURIST_ABOUT_NOSHOW_USED = 9
    NOTIFY_OWNER_ABOUT_NOSHOW_CANCELLATION = 10
    NOTIFY_TOURIST_ABOUT_NOSHOW_CANCELLATION = 11

    EMAIL_TYPES = (
        (NOTIFY_OWNER_ABOUT_NEW_BOOKING, 'notify owner about new booking'),
        (NOTIFY_OWNER_ABOUT_BOOKING_APPROVAL, 'notify owner about booking approval'),
        (NOTIFY_TOURIST_ABOUT_BOOKING_APPROVAL, 'notify tourist about booking approval'),
        (NOTIFY_OWNER_ABOUT_BOOKING_MANUAL_REJECT, 'notify owner about booking manual reject'),
        (NOTIFY_TOURIST_ABOUT_BOOKING_MANUAL_REJECT, 'notify tourist about booking manual reject'),
        (NOTIFY_OWNER_ABOUT_BOOKING_AUTO_REJECT, 'notify owner about booking auto reject'),
        (NOTIFY_TOURIST_ABOUT_BOOKING_AUTO_REJECT, 'notify tourist about booking auto reject'),
        (NOTIFY_OWNER_ABOUT_NOSHOW_USED, 'notify owner about noshow used'),
        (NOTIFY_TOURIST_ABOUT_NOSHOW_USED, 'notify tourist about noshow used'),
        (NOTIFY_OWNER_ABOUT_NOSHOW_CANCELLATION, 'notify owner about noshow cancellation'),
        (NOTIFY_TOURIST_ABOUT_NOSHOW_CANCELLATION, 'notify tourist about noshow cancellation')
    )

    EMAIL_TYPES_INDEXES = [t[0] for t in EMAIL_TYPES]

    TOURIST_EMAILS = [
        NOTIFY_TOURIST_ABOUT_BOOKING_APPROVAL,
        NOTIFY_TOURIST_ABOUT_BOOKING_MANUAL_REJECT,
        NOTIFY_TOURIST_ABOUT_BOOKING_AUTO_REJECT,
        NOTIFY_TOURIST_ABOUT_NOSHOW_USED,
        NOTIFY_TOURIST_ABOUT_NOSHOW_CANCELLATION
    ]

    OWNER_EMAILS = [
        NOTIFY_OWNER_ABOUT_NEW_BOOKING,
        NOTIFY_OWNER_ABOUT_BOOKING_APPROVAL,
        NOTIFY_OWNER_ABOUT_BOOKING_MANUAL_REJECT,
        NOTIFY_OWNER_ABOUT_BOOKING_AUTO_REJECT,
        NOTIFY_OWNER_ABOUT_NOSHOW_USED,
        NOTIFY_OWNER_ABOUT_NOSHOW_CANCELLATION
    ]

    email_type = models.IntegerField('Email type', choices=EMAIL_TYPES, unique=True)

    translations = TranslatedFields(
        subject=models.CharField('Subject', max_length=255, help_text=mark_safe(
            "You can use here these tags (these values will taken from recipient of this letter):<br>"
            "[EMAIL] - recipient email<br>"
            "[LOGIN] - recipient login<br>"
            "[FIRST_NAME] - recipient first name (can be empty)<br>"
            "[LAST_NAME] - recipient last name (can be empty)")),
        email_body=RichTextField('Email body', help_text=mark_safe(
            "You can use here these tags in every email:<br>"
            "[RECIPIENT_EMAIL] - recipient email<br>"
            "[RECIPIENT_USERNAME] - recipient username<br>"
            "[RECIPIENT_FIRST_NAME] - recipient first name (can be empty)<br>"
            "[RECIPIENT_LAST_NAME] - recipient last name (can be empty)<br>"
            "[ORDER_ITEM_ID] - booking unique identifier<br>"
            "[DATES] - booking dates<br>"
            "[BOOKINGS_LINK] - bookings link for email recipient "
            "(you can use it as URL during creation of new link but you should set the PROTOCOL of it to 'other')<br>"
            "[ITEM_DESCRIPTION] - item description depended from item<br>"
            "[QUANTITY] - number of items in booking (equals 1 for apartments and item-based productions)<br>"
            "[PRICE] - total price of this booking (quantity * price per item)<br>"
            "All emails to business owners can contain also:<br>"
            "[TOURIST_ID] - tourist unique identifier<br>"
            "Email to owner about booking approval can also contain:<br>"
            "[TOURIST_EMAIL] - tourist email<br>"
            "[TOURIST_PHONE] - tourist phone<br>"
            "Email to tourist about booking approval can also contain:<br>"
            "[OWNER_EMAIL] - owner email<br>"
            "[OWNER_PHONE] - owner phone<br>"
            "Email about owner inactivity can also contain:<br>"
            "[HOURS_OF_INACTIVITY] - owner was inactive during this number of hours so the booking was rejected")),
    )

    objects = BookingEmailTemplateManager()

    class Meta:
        verbose_name = 'Booking Email Template'
        verbose_name_plural = 'Booking Email Templates'

    def __unicode__(self):
        return self.get_email_type_display()
