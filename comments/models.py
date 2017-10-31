from django.db import models
from products.models import Vendor
# Create your models here.
class Comment(models.Model):
    """docstring for Comment"""
    """ 설명 """
    vendor = models.ForeignKey(Vendor)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.vendor, self.id)

