from django import template


register = template.Library()

@register.assignment_tag
def get_price_for_dates(item, start_date, end_date, quantity=1):
    return item.calculate_price_for_booking(start_date, end_date, quantity)

@register.assignment_tag
def get_total_price_and_price_per_day_for_dates(item, start_date, end_date, quantity=1):
    total, per_day = item.calculate_total_price_and_price_per_day(start_date, end_date, quantity)
    return {'total_price': total, 'price_per_day': per_day}


@register.filter("date_diff", is_safe=False)
def date_diff_filter(start, end):
    """Returns date difference in number of days from first argument to the last."""
    if not start or not end:
        return ''
    return (end - start).days


@register.assignment_tag(takes_context=True)
def get_name_for_item(context):
    curr_item = context['item']
    return "i_%d" % curr_item.pk

@register.inclusion_tag("entertainment/includes/item_num_select.html", takes_context=True)
def generate_select_for_item(context):
    curr_item = context['item']
    if curr_item.is_one_time_item:
        option_number = 2
    else:
        item_num = curr_item.number
        option_number = item_num if item_num < 10 else 10
    return {
        "name": "i_%d" % curr_item.pk,
        "options": [i for i in range(0, option_number + 1)]
    }

