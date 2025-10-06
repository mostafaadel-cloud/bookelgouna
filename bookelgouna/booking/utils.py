from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from .models import Cart, OrderItem


def get_cart(request):
    if request.user.is_authenticated():
        cart = Cart.objects.get(user=request.user)
    else:
        cart = Cart.objects.get(session_key=request.session.session_key)
    return cart


def get_order_item_with_this_item_in_dates(item, from_date, to_date):
    ct = ContentType.objects.get_for_model(item)
    order_items = OrderItem.objects.filter(content_type=ct, object_id=item.pk).filter(
        Q(from_date__lte=from_date, to_date__gt=from_date) |
        Q(from_date__lt=to_date, to_date__gte=to_date) |
        Q(from_date__lte=from_date, to_date__gte=to_date) |
        Q(from_date__gte=from_date, to_date__lte=to_date))
    if len(order_items) >= 1:
        return order_items[0]
    else:
        return None
