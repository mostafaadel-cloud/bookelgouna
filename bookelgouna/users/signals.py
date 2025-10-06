from allauth.account.signals import user_logged_in

from django.dispatch import receiver


@receiver(user_logged_in)
def process_user_logged_in(request, user, **kwargs):
    if not hasattr(request, 'old_cart_id'):
        return
    from booking.models import Cart, CartItem
    delattr(request, '_cached_cart')
    request.cart = Cart.objects.get_cart_from_request(request)
    CartItem.objects.filter(cart_id=request.old_cart_id).update(cart_id=request.cart.id)
