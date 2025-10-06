from __future__ import absolute_import

from celery import shared_task
import logging

from .models import OrderItem

logger = logging.getLogger('booking')

@shared_task
def reject_orderitem(orderitem_pk):
    try:
        orderitem = OrderItem.objects.get(pk=orderitem_pk)
    except OrderItem.DoesNotExist:
        logger.warning('No order item with this pk: %s' % orderitem_pk)
        return False
    else:
        result = orderitem.reject_due_to_owner_inactivity()
        if result:
            logger.info('Order item with pk: %s was rejected due to owner inactivity.' % orderitem_pk)
        return result
