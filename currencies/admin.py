from django.contrib import admin
from currencies.models import BaseCurrency,ForeignCurrency

## ForeignCurrency (inline)
class ForeignCurrencyInline(admin.TabularInline):
    model = ForeignCurrency
    fields = ('code','name','symbol','invert_rate')
    extra = 3

## BaseCurrency
class BaseCurrencyAdmin(admin.ModelAdmin):
    inlines = [ForeignCurrencyInline]
    def save_model(self, request, obj, form, change):
        obj.invalidate()
admin.site.register(BaseCurrency,BaseCurrencyAdmin)
