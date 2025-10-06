from django.utils.functional import SimpleLazyObject

from .models import Cart


def get_cart(request):
    if not hasattr(request, '_cached_cart'):
        request._cached_cart = Cart.objects.get_cart_from_request(request)
    return request._cached_cart


class CartMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Cart middleware requires django authentication middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.auth.middleware.AuthenticationMiddleware'."

        request.cart = SimpleLazyObject(lambda: get_cart(request))
