from django import forms

def currency_form(base,default=None,mini=False):
    if mini:
        choices = [
            (f.code,f.symbol) for f in [base]+sorted(
                list(base.foreign_currencies.all()),
                cmp=lambda x,y: cmp(len(x.symbol),len(y.symbol)) or cmp(x.symbol,y.symbol)
            )
        ]
    else:
        choices = [
            (f.code,'%s (%s)' %(f.name,f.symbol)) for f in [base]+list(base.foreign_currencies.all())
        ]
    default = default or base.code
    class TheForm(forms.Form):
        currency = forms.ChoiceField(choices=choices,label=u'')
    return TheForm({'currency':default}) 
