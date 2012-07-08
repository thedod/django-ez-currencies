Django currencies lets you convert prices to foreign currencies for display purposes.

* The assumption is that all prices are kept in a single currency (called the `base currency`).

* The user can select to display these prices in one of the foreign currencies you offer.
  Their rates will be fetched from Yahoo! Finance (and cached).

* You can use the `to_currency` template filter to display a price in a currency (base or foreign).

* You can use the `currency_form` and `currency_mini_form` template filters in order to
  render a currency selection form for the user.

### Installation

* Copy currencies/ to your project's folders
* Add 'currencies' to your INSTALLED_APPS at settings.py
* Do `./manage.py syncdb`
* Optional: do `./manage.py loaddata currencies defaults` to load sample initial data

### Admin

You need to have a **single** `Base currency` (if you have more than one, only the first one will be used):

* Enter ISO code (e.g. 'USD'), name (e.g. 'US Dollar'), and symbol (e.g. '$')
* Decide how long (in minutes) before cached rates expire.
* Define foreign currencies. For each:
  * ISO code, name, and symbol
  * Whether to invert the rate (if rate<1, inverting it should bring a more accurate rate).

### Template filters

* You need to `{% load currency_filters %}`
* You can convert a price with `{{ 23.23|to_currency:'EUR' }}`.
  This would also prefix the currency's symbol (so it also makes sense to use this for the base currency).
* You can render a currency selection form with
  `{% with f='GBP'|currency_form %}{{ f.as_p }}{% endwith %}`
  this will render a `select` tag of all foreign currencies, with GBP as the selected option.
* `{% with f=user.profile.currency|currency_mini_form %}{{ f.as_li }}{% endwith %}`
  does something similar, but option text is only the currency symbol
  (e.g. `$` instead of `US Dollar ($)`).

### Note

You should inform the user that prices in foreign currencies are only estimates,
and the payment processor (e.g. paypal) might use a different rate for the exchange.

### Acknowledgement

Thanks to Alexander Teves for the [Yahoo! Finance interface](https://github.com/alexanderteves/CurrencyExchangeRate)
