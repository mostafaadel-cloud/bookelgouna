from django import template


register = template.Library()

@register.assignment_tag
def get_price_for_dates(price_category, start_date, end_date, quantity=1):
    if price_category.prices.exists():
        return price_category.calculate_price_for_booking(start_date, end_date, quantity)
    else:
        return 'n/a'