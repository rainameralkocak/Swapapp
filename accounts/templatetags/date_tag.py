from django import template
from datetime import datetime
import locale

register = template.Library()

@register.simple_tag
def formatted_date():
    # Set the locale to Turkish
    locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')

    # Get the current date and format it
    now = datetime.now()
    return now.strftime("%d.%m.%Y %A")