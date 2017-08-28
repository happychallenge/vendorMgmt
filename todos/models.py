from django.db import models

# Create your models here.
class Todo(models.Model):
    """docstring for Todo"""
    """ 설명 """
    URGENT = 'URGENT'
    NORMAL = 'NORMAL'
    ETYPE = (
        (NORMAL, 'NORMAL'),
        (URGENT, 'URGENT'),
    )

    name = models.CharField(max_length=30)
    content = models.TextField(blank=True, null=True)
    duedate = models.DateField()
    etype = models.CharField(max_length=10, choices=ETYPE, default=NORMAL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
