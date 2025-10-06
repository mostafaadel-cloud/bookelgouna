# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management import BaseCommand

from email_templates.models import BookingEmailTemplate


class Command(BaseCommand):
    def handle(self, *args, **options):
        BookingEmailTemplate.objects.language('en').get_or_create(
            email_type=BookingEmailTemplate.NOTIFY_OWNER_ABOUT_NEW_BOOKING,
            defaults={
                'subject': 'New booking',
                'email_body': '<p>New booking was created. Order id: [ORDER_ITEM_ID]. Tourist id: [TOURIST_ID]. Dates: [DATES]. Item description: [ITEM_DESCRIPTION]. Quantity: [QUANTITY]. Price: [PRICE].</p><p>Observe this and other bookings via link: <a href="[BOOKINGS_LINK]">[BOOKINGS_LINK]</a></p>'
            }
        )
        BookingEmailTemplate.objects.language('en').get_or_create(
            email_type=BookingEmailTemplate.NOTIFY_OWNER_ABOUT_BOOKING_APPROVAL,
            defaults={
                'subject': 'New approval',
                'email_body': '<p>You have approved a booking. Order id: [ORDER_ITEM_ID]. Tourist id: [TOURIST_ID]. Tourist email: [TOURIST_EMAIL]. Tourist phone: [TOURIST_PHONE]. Dates: [DATES]. Item description: [ITEM_DESCRIPTION]. Quantity: [QUANTITY]. Price: [PRICE].</p><p>Observe this and other bookings via link: <a href="[BOOKINGS_LINK]">[BOOKINGS_LINK]</a></p>'
            }
        )
        BookingEmailTemplate.objects.language('en').get_or_create(
            email_type=BookingEmailTemplate.NOTIFY_TOURIST_ABOUT_BOOKING_APPROVAL,
            defaults={
                'subject': 'New approval',
                'email_body': '<p>Your booking was approved by service owner. Order id: [ORDER_ITEM_ID]. Owner email: [OWNER_EMAIL]. Owner phone: [OWNER_PHONE]. Dates: [DATES]. Item description: [ITEM_DESCRIPTION]. Quantity: [QUANTITY]. Price: [PRICE].</p><p>Observe this and other bookings via link: <a href="[BOOKINGS_LINK]">[BOOKINGS_LINK]</a></p>'
            }
        )
        BookingEmailTemplate.objects.language('en').get_or_create(
            email_type=BookingEmailTemplate.NOTIFY_OWNER_ABOUT_BOOKING_MANUAL_REJECT,
            defaults={
                'subject': 'Booking was rejected',
                'email_body': '<p>You have rejected a booking. Order id: [ORDER_ITEM_ID]. Tourist id: [TOURIST_ID]. Dates: [DATES]. Item description: [ITEM_DESCRIPTION]. Quantity: [QUANTITY]. Price: [PRICE].</p><p>Observe this and other bookings via link: <a href="[BOOKINGS_LINK]">[BOOKINGS_LINK]</a></p>'
            }
        )
        BookingEmailTemplate.objects.language('en').get_or_create(
            email_type=BookingEmailTemplate.NOTIFY_TOURIST_ABOUT_BOOKING_MANUAL_REJECT,
            defaults={
                'subject': 'Booking was rejected',
                'email_body': '<p>Your booking was rejected by service owner. Order id: [ORDER_ITEM_ID]. Dates: [DATES]. Item description: [ITEM_DESCRIPTION]. Quantity: [QUANTITY]. Price: [PRICE].</p><p>Observe this and other bookings via link: <a href="[BOOKINGS_LINK]">[BOOKINGS_LINK]</a></p>'
            }
        )
        BookingEmailTemplate.objects.language('en').get_or_create(
            email_type=BookingEmailTemplate.NOTIFY_OWNER_ABOUT_BOOKING_AUTO_REJECT,
            defaults={
                'subject': 'Booking was rejected automatically',
                'email_body': '<p>The system has automatically rejected the booking. Reason: your inactivity in last [HOURS_OF_INACTIVITY] hours. Order id: [ORDER_ITEM_ID]. Tourist id: [TOURIST_ID]. Dates: [DATES]. Item description: [ITEM_DESCRIPTION]. Quantity: [QUANTITY]. Price: [PRICE].</p><p>Observe this and other bookings via link: <a href="[BOOKINGS_LINK]">[BOOKINGS_LINK]</a></p>'
            }
        )
        BookingEmailTemplate.objects.language('en').get_or_create(
            email_type=BookingEmailTemplate.NOTIFY_TOURIST_ABOUT_BOOKING_AUTO_REJECT,
            defaults={
                'subject': 'Booking was rejected automatically',
                'email_body': '<p>The system has automatically rejected your booking. Reason: business owner inactivity. Order id: [ORDER_ITEM_ID]. Dates: [DATES]. Item description: [ITEM_DESCRIPTION]. Quantity: [QUANTITY]. Price: [PRICE].</p><p>Observe this and other bookings via link: <a href="[BOOKINGS_LINK]">[BOOKINGS_LINK]</a></p>'
            }
        )
        BookingEmailTemplate.objects.language('en').get_or_create(
            email_type=BookingEmailTemplate.NOTIFY_OWNER_ABOUT_NOSHOW_USED,
            defaults={
                'subject': 'No show status',
                'email_body': '<p>You have changed booking status to "No Show". Order id: [ORDER_ITEM_ID]. Tourist id: [TOURIST_ID]. Dates: [DATES]. Item description: [ITEM_DESCRIPTION]. Quantity: [QUANTITY]. Price: [PRICE].</p><p>Observe this and other bookings via link: <a href="[BOOKINGS_LINK]">[BOOKINGS_LINK]</a></p>'
            }
        )
        BookingEmailTemplate.objects.language('en').get_or_create(
            email_type=BookingEmailTemplate.NOTIFY_TOURIST_ABOUT_NOSHOW_USED,
            defaults={
                'subject': 'No show status',
                'email_body': '<p>Your booking has got "No Show" status. Order id: [ORDER_ITEM_ID]. Dates: [DATES]. Item description: [ITEM_DESCRIPTION]. Quantity: [QUANTITY]. Price: [PRICE].</p><p>Observe this and other bookings via link: <a href="[BOOKINGS_LINK]">[BOOKINGS_LINK]</a></p>'
            }
        )
        BookingEmailTemplate.objects.language('en').get_or_create(
            email_type=BookingEmailTemplate.NOTIFY_OWNER_ABOUT_NOSHOW_CANCELLATION,
            defaults={
                'subject': 'No show status cancellation',
                'email_body': '<p>You have cancelled "No Show" status of booking. Order id: [ORDER_ITEM_ID]. Tourist id: [TOURIST_ID]. Dates: [DATES]. Item description: [ITEM_DESCRIPTION]. Quantity: [QUANTITY]. Price: [PRICE].</p><p>Observe this and other bookings via link: <a href="[BOOKINGS_LINK]">[BOOKINGS_LINK]</a></p>'
            }
        )
        BookingEmailTemplate.objects.language('en').get_or_create(
            email_type=BookingEmailTemplate.NOTIFY_TOURIST_ABOUT_NOSHOW_CANCELLATION,
            defaults={
                'subject': 'No show status cancellation',
                'email_body': '<p>Your booking is approved again. "No Show" status was cancelled. Order id: [ORDER_ITEM_ID]. Dates: [DATES]. Item description: [ITEM_DESCRIPTION]. Quantity: [QUANTITY]. Price: [PRICE].</p><p>Observe this and other bookings via link: <a href="[BOOKINGS_LINK]">[BOOKINGS_LINK]</a></p>'
            }
        )
