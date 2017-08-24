from django.db import models
from django.conf import settings

class Location(models.Model):
    """docstring for Location"""
    """ 설명 """
    en_name = models.CharField(max_length=20)
    cn_name = models.CharField(max_length=10)
    class Meta:
        ordering = ['en_name']

    def __str__(self):
        return self.en_name.upper()


# Create your models here.
class Vendor(models.Model):
    """docstring for Provider"""
    """ 설명 """
    ACTIVE = 'A'
    INACTIVE = 'I'
    BANKRUPT = 'B'
    STATUS = (
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'),
        (BANKRUPT, 'BANKRUPT'),
    )

    TRADING = 'T'
    MANUFACTURER = 'M'
    MIXING = 'X'
    COMPANYTYPE = (
        (TRADING, 'TRADING'),
        (MANUFACTURER, 'MANUFACTURER'),
        (MIXING, 'MIXING'),
    )

    CURRENT = 'CURRENT'
    OLD = 'OLD'
    NO = 'NO'
    GPRELATION = (
        (CURRENT, 'CURRENT'),
        (OLD, 'OLD'),
        (NO, 'NO'),
    )

    cn_name = models.CharField(max_length=50, verbose_name='CHINESE NAME')
    en_name = models.CharField(max_length=50, verbose_name='ENGLISH NAME')
    simple_name = models.CharField(max_length=20, verbose_name='SIMPLE NAME', blank=True, null=True,)
    cn_address = models.CharField(max_length=100, blank=True, null=True, verbose_name='CHINESE ADDRESS')
    en_address = models.CharField(max_length=200, blank=True, null=True, verbose_name='ENGLISH ADDRESS')
    homepage = models.URLField(blank=True, null=True)
    tel = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default=ACTIVE)
    gprelation = models.CharField(max_length=20, choices=GPRELATION, default=CURRENT, verbose_name='GP RELATION')
    companytype = models.CharField(max_length=20, choices=COMPANYTYPE, default=MANUFACTURER)
    location = models.ForeignKey(Location, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    comments = models.TextField(blank=True, null=True)
    product_list = models.FileField(upload_to='product_list/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [ 'en_name' ]

    def __str__(self):
        return self.en_name.upper()

    


class Tag(models.Model):
    tag = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag


class Contact(models.Model):
    """docstring for Contact"""
    """ Contact """
    PRESIDENT = 'P'
    VICEPRESIDENT = 'VP'
    SALESDIRECTOR = 'SD'
    SALESMANAGER = 'SM'
    SALESMAN = 'S'
    ROLE = (
        (PRESIDENT, 'President'),
        (VICEPRESIDENT, 'Vice-President'),
        (SALESDIRECTOR, 'SalesDirector'),
        (SALESMANAGER, 'SalesManager'),
        (SALESMAN, 'SalesMan'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL,blank=True, null=True)
    vendor = models.ForeignKey(Vendor)
    cn_name = models.CharField(max_length=30, verbose_name='CHINESE NAME')
    en_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='ENGLISH NAME')
    role = models.CharField(max_length=2, choices=ROLE, default=SALESMAN)
    picture = models.ImageField(upload_to='contact_profile/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=30, blank=True, null=True)
    fixed = models.CharField(max_length=30, blank=True, null=True)
    wechat = models.CharField(max_length=30, blank=True, null=True)
    qq = models.CharField(max_length=30, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['en_name']

    def __str__(self):
        return self.en_name


class Category(models.Model):
    """docstring for Category"""
    cn_name = models.CharField(max_length=30)
    en_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.en_name.upper()

class Product(models.Model):
    """docstring for Product"""
    """ 설명 """
    cn_name = models.CharField(max_length=100, verbose_name='CHINESE NAME')
    en_name = models.CharField(max_length=100, verbose_name='ENGLISH NAME')
    cas_no = models.CharField(max_length=30, verbose_name='CAS NO', blank=True, null=True)
    category = models.ForeignKey(Category)

    cn_hscode = models.CharField(max_length=15, verbose_name='중국 HS CODE', blank=True, null=True)
    ko_hscode = models.CharField(max_length=15, verbose_name='한국 HS CODE', blank=True, null=True)
    etc_hscode = models.CharField(max_length=15, verbose_name='ETC HS CODE', blank=True, null=True)
    rate_taxrefund = models.FloatField(max_length=100, verbose_name='RATE of TAX REFUND(%)', blank=True, null=True)

    molnumber = models.FloatField(max_length=100, verbose_name='분자량', blank=True, null=True)
    chemequal = models.CharField(max_length=100, verbose_name='화학식', blank=True, null=True)
    chemstructure = models.ImageField(verbose_name='구조식', blank=True, null=True, upload_to='chemicalstructure/')
    
    usage = models.TextField(max_length=500, verbose_name='용도', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [ 'en_name', ]

    def __str__(self):
        return self.en_name.upper()

    # def get_vendor_list(self):
    #     return Sourcing.objects.filter(vendorproduct__product=self).annotate()


POWDER = 'POWDER'
GRANULAR = 'GRANULAR'
LIQUID = 'LIQUID'
TYPE = (
    (POWDER, 'POWDER'),
    (GRANULAR, 'GRANULAR'),
    (LIQUID, 'LIQUID'),
)

class Packing(models.Model):
    """docstring for Packing"""
    """ 설명 """

    CARTON = 'CARTON'
    BAG = 'BAG'
    DRUM = 'DRUM'
    CYLINDER = 'CYLINDER'
    EXTRA = 'EXTRA'
    PACKINGTYPE = (
        (CARTON, 'CARTON'),
        (BAG, 'BAG'),
        (DRUM, 'DRUM'),
        (CYLINDER, 'CYLINDER'),
        (EXTRA, 'EXTRA'),
    )

    product = models.ForeignKey(Product)
    ptype = models.CharField(max_length=10, choices=TYPE, default=POWDER)
    packing_type = models.CharField(max_length=10, choices=PACKINGTYPE, default=BAG)
    unit_weight = models.IntegerField()
    pallet_weight = models.IntegerField(default=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.product, self.ptype)


    
class VendorProduct(models.Model):
    """docstring for CompcanyProduct"""
    
    vendor = models.ForeignKey(Vendor)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ptype = models.CharField(max_length=10, choices=TYPE, default=POWDER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('vendor', 'product', 'ptype'),)
        ordering = [ 'vendor', 'product' ]

    def __str__(self):
        return "{} | {} ({})".format(self.vendor, self.product, self.ptype)
    

class Quotation(models.Model):
    """docstring for Quotation"""
    """ Quotation """
    VALID = 'V'
    INVALID = 'I'
    STATUS = (
        (VALID, 'VALID'),
        (INVALID, 'IN-VALID'),
    )

    RMB = 'R'
    DOLLAR = '$'
    CURRENCY = (
        (RMB, 'RMB'),
        (DOLLAR, 'DOLLAR'),
    )

    CASH = 'CASH'
    THIRTY = '30%PREPAY, 70%LATER'
    TT30 = 'T/T 30 DAYS'
    TT45 = 'T/T 45 DAYS'
    TT60 = 'T/T 60 DAYS'
    TT90 = 'T/T 90 DAYS'
    PAYTERM = (
        (CASH, 'CASH'),
        (THIRTY, '30%PREPAY, 70%LATER'),
        (TT30, 'T/T 30 DAYS'),
        (TT45, 'T/T 45 DAYS'),
        (TT60, 'T/T 60 DAYS'),
        (TT90, 'T/T 90 DAYS'),
    )

    vendorproduct = models.ForeignKey(VendorProduct)
    price = models.FloatField()
    currency = models.CharField(max_length=1, choices=CURRENCY, default=DOLLAR)
    payterm = models.CharField(max_length=20, choices=PAYTERM, default=TT60)
    quote_date = models.DateTimeField(auto_now_add=True)
    effective_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS, default=VALID)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        ordering = [ 'status', 'price' ]

    def __str__(self):
        return "{}".format(self.vendorproduct)


class Sourcing(models.Model):
    """docstring for Quotation"""
    """ Quotation """
    VALID = 'V'
    INVALID = 'I'
    STATUS = (
        (VALID, 'VALID'),
        (INVALID, 'IN-VALID'),
    )

    CASH = 'CASH'
    THIRTY = '30%PREPAY, 70%LATER'
    TT30 = 'T/T 30 DAYS'
    TT45 = 'T/T 45 DAYS'
    TT60 = 'T/T 60 DAYS'
    TT90 = 'T/T 90 DAYS'
    PAYTERM = (
        (CASH, 'CASH'),
        (THIRTY, '30%PREPAY, 70%LATER'),
        (TT30, 'T/T 30 DAYS'),
        (TT45, 'T/T 45 DAYS'),
        (TT60, 'T/T 60 DAYS'),
        (TT90, 'T/T 90 DAYS'),
    )

    vendorproduct = models.ForeignKey(VendorProduct)
    buying_price = models.FloatField()
    usd_price = models.FloatField(blank=True, null=True)
    sales_price = models.FloatField(blank=True, null=True)
    payterm = models.CharField(max_length=20, choices=PAYTERM, default=CASH)
    quote_date = models.DateTimeField(auto_now_add=True)
    effective_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS, default=VALID)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        ordering = [ '-status', '-quote_date', ]

    def __str__(self):
        return "{}".format(self.vendorproduct)
    