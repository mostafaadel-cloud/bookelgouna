def cart_info(request):
    return {'cart_items_count': request.cart.items.count()}
