from django import template
from currencies.models import BaseCurrency
from currencies import forms

register = template.Library()

def base_currency():
    return BaseCurrency.objects.all()[0]

@register.filter(is_safe=True)
def to_currency(price,currency):
    b = base_currency()
    c = b.get_currency(currency)
    return (len(c.symbol)>1 and u' ' or u'').join(
        (c.symbol,unicode(b.to_currency(currency,price)))
    )

@register.filter
def currency_form(default):
    return forms.currency_form(base_currency(),default)
