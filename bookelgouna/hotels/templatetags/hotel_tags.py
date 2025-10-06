from django import template
from django.template.defaultfilters import floatformat


register = template.Library()

@register.assignment_tag
def get_price_for_dates_prefetched(price_category, start_date, end_date, quantity=1):
    if price_category.prices.exists():
        return price_category.calculate_total_price_with_prefetched_prices(start_date, end_date, quantity)
    else:
        return 'n/a'

@register.simple_tag
def get_price_for_dates(price_category, start_date, end_date, quantity=1):
    if price_category.prices.exists():
        return floatformat(price_category.calculate_price_for_booking(start_date, end_date, quantity))
    else:
        return 'n/a'


@register.simple_tag
def diff_between_dates(start_date, end_date):
    return (end_date - start_date).days


@register.filter("date_diff", is_safe=False)
def date_diff_filter(start, end):
    """Returns date difference in number of days from first argument to the last."""
    if not start or not end:
        return ''
    return (end - start).days


@register.assignment_tag
def hide_this_price_extra_form(forloop, subform, prices_initial_form_count):
    is_first = forloop['first']
    has_errors = bool(subform.errors)
    has_changed = subform.has_changed()
    show_it = has_changed or has_errors or (is_first and not prices_initial_form_count)
    return not show_it


@register.inclusion_tag("hotels/includes/price_category_select.html", takes_context=True)
def generate_select_for_price_category(context):
    curr_room = context['room']
    curr_price_category = context['price_category']
    room_num = curr_room.allotment
    option_number = room_num if room_num < 10 else 10
    return {
        "name": "pc_%d" % curr_price_category.pk,
        "options": [i for i in range(0, option_number + 1)]
    }

