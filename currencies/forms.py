from django import forms

def currency_form(base,default=None):
    choices = [(f.code,'%s (%s)' %(f.name,f.symbol)) for f in [base]+list(base.foreign_currencies.all())]
    default = default or base.code
    class TheForm(forms.Form):
        currency = forms.ChoiceField(choices=choices,label=u'')
    return TheForm({'currency':default}) 
