from django.db import models
import datetime,urllib2,decimal,logging
logger=logging.getLogger('django')

### ========= BaseCurrency
class BaseCurrency(models.Model):
    code = models.CharField('Currency code',max_length=3,unique=True)
    name = models.CharField('Name',max_length=42)
    symbol = models.CharField('Symbol',max_length=3)
    expiry_minutes = models.PositiveIntegerField('Rate expiry time (minutes)',default=60)

    def get_currency(self,code):
        if code==self.code:
            return self
        return self.foreign_currencies.get(code=code)
    def to_currency(self,to_currency,base_price=1):
        if to_currency==self.code:
            result = base_price
        else:
            try:
                c = self.get_currency(to_currency)
            except:
                logger.error('Unknow currency code "%s"' % to_currency)
                return 0
            rate = c.rate
            if not rate:
                return 0
            if c.invert_rate:
                result = decimal.Decimal(base_price)*rate
            else:
                result = decimal.Decimal(base_price)/rate
        return decimal.Decimal(result).quantize(decimal.Decimal('0.01'))
    def invalidate(self):
        self.save()
        for fc in self.foreign_currencies.all():
            fc.invalidate()
    class Meta:
        verbose_name = 'Base currency'
        verbose_name_plural = 'Base currencies'
    def __unicode__(self):
        return self.code

### ========= ForeignCurrency
class ForeignCurrency(models.Model):
    code = models.CharField('Code',max_length=3,unique=True)
    name = models.CharField('Name',max_length=42)
    symbol = models.CharField('Symbol',max_length=3)
    invert_rate = models.BooleanField('Invert rate',
        help_text= "check this if rate<1, for better accuracy")
    base = models.ForeignKey(BaseCurrency,verbose_name='Base currency',related_name='foreign_currencies')
    ### Internal fields. Excluded from admin.
    _rate = models.DecimalField('Rate',max_digits=8,decimal_places=4,default=0)
    _expires = models.DateTimeField('Expiry',null=True,blank=True)
    def _codes(self):
        return self.invert_rate and (
            self.base.code,self.code) or (
            self.code,self.base.code)
    ### The rate read-only property
    def get_rate(self):
        now = datetime.datetime.now()
        if self._expires and self._expires > now:
            return self._rate
        try:
            url = 'http://finance.yahoo.com/d/quotes.csv?s=%s%s=X&f=l1' % self._codes()
            rate = decimal.Decimal(urllib2.urlopen(url).read().rstrip())
        except Exception, e:
            logger.error(e)
            return self._rate # That's the best we can do
        if not rate:
            logger.error('Bad currency code(s): %s/%s' % self._codes())
        self._rate = rate
        self._expires = now+datetime.timedelta(
            minutes=self.base.expiry_minutes)
        self.save()
        return self._rate
    rate = property(get_rate)
    def invalidate(self):
        self._expires = None
        self._rate = 0
        self.save()
    class Meta:
        verbose_name = 'Foreign currency'
        verbose_name_plural = 'Foreign currencies'
        ordering = ['name']
    def __unicode__(self):
        return u'/'.join(self._codes())
