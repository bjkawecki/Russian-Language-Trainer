import datetime
import logging

from dateutil.relativedelta import relativedelta
from django import template

register = template.Library()

logger = logging.getLogger("django")


@register.filter
def divide(value, arg):
    try:
        divided_value = int(value) / int(arg)
        return f"{divided_value:g}"
    except (ValueError, ZeroDivisionError) as e:
        logger.error(e)
        return None


@register.filter
def next_bca(value):
    return value + relativedelta(months=1) - datetime.timedelta(days=1)
