from django.contrib import admin
from currencies.models import BaseCurrency,ForeignCurrency

def currency_rate(obj):
    return obj.rate
currency_rate.short_description = 'Rate'

def currencies(obj):
    return unicode(obj)
currencies.short_description = 'Currencies'

## ForeignCurrency
class ForeignCurrencyAdmin(admin.ModelAdmin):
    list_display = (currencies,'invert_rate',currency_rate)
    list_editable = ('invert_rate',)
    def save_model(self, request, obj, form, change):
        obj.invalidate()
admin.site.register(ForeignCurrency,ForeignCurrencyAdmin)

## ForeignCurrency (inline)
class ForeignCurrencyInline(admin.TabularInline):
    model = ForeignCurrency
    fields = ('code','name','symbol','invert_rate')
    extra = 3

## BaseCurrency
class BaseCurrencyAdmin(admin.ModelAdmin):
    inlines = [ForeignCurrencyInline]
    def save_model(self, request, obj, form, change):
        obj.save()
        obj.invalidate()
admin.site.register(BaseCurrency,BaseCurrencyAdmin)
