from django.db import models

# Create your models here.
class Event(models.Model):
    """docstring for Event"""
    """ 설명 """

    CONTRACT = 'CONTRACT'
    SHIPPING = 'SHIPPING'
    PAYMENT = 'PAYMENT'
    TAXREFUND = 'TAXREFUND'
    TYPE = (
        (CONTRACT, 'CONTRACT'),
        (SHIPPING, 'SHIPPING'),
        (PAYMENT, 'PAYMENT'),
        (TAXREFUND, 'TAXREFUND'),
    )

    name = models.CharField(max_length=50)
    num = models.PositiveIntegerField()
    etype = models.CharField(max_length=10, choices=TYPE)
    event_date = models.DateField()

    money = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=1, default='$')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
