# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def get_desc(app, item):
    if app == "hotels":
        return 'Room "%(room_type)s" (%(room_adults_num)d adults, %(room_child_num)d children) in Hotel "%(hotel_name)s"' % \
               {'room_type': item.type.translations.first().name, 'room_adults_num': item.adults,
                'room_child_num': item.children, 'hotel_name': item.service.translations.first().title}
    elif app == "apartments":
        return '%(apt_type)s "%(apt_name)s" (%(apt_rooms_num)d rooms, %(apt_adults_num)d adults, %(apt_child_num)d children)' % \
               {'apt_type': item.get_type_display(), 'apt_name': item.translations.first().title,
                'apt_rooms_num': item.number_of_rooms, 'apt_adults_num': item.adults, 'apt_child_num': item.children}
    else:
        return ""


def generate_orderitem_desc(apps, schema_editor):
    OrderItem = apps.get_model('booking', 'OrderItem')
    model_classes = {}
    for orderitem in OrderItem.objects.all():
        ct = orderitem.content_type
        app = ct.app_label
        model = ct.model
        key = "%s.%s" % (app, model)
        if key in model_classes:
            model_class = model_classes[key]
        else:
            model_class = apps.get_model(app, model)
            model_classes[key] = model_class
        try:
            price_category = model_class.objects.get(pk=orderitem.object_id)
        except model_class.DoesNotExist:
            orderitem.item_desc = "broken"
        else:
            orderitem.item_desc = get_desc(app, price_category.item)
        orderitem.save()


def stub(apps, schema_editor):
    OrderItem = apps.get_model('booking', 'OrderItem')
    for orderitem in OrderItem.objects.all():
        orderitem.item_desc = ""
        orderitem.save()


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_orderitem_item_desc'),
        ('hotels', '0049_room_cart_crop'),
        ('apartments', '0006_apartment_area'),
    ]

    operations = [
        migrations.RunPython(generate_orderitem_desc, stub),
    ]
