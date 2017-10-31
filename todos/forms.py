from django import forms
from django.contrib.admin import widgets 

from bootstrap_datepicker.widgets import DatePicker

from .models import Todo

class TodoForm(forms.ModelForm):
    duedate = forms.DateField(
            widget=DatePicker(options={
                    "format": "yyyy-mm-dd","autoclose": True}))
    class Meta:
        model = Todo
        fields = "__all__"
        # widgets = { "duedate": forms.DateInput(attrs={'class': 'dtepicker'})}
