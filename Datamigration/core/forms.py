from django import forms
from .models import *


class DBImportForm(forms.ModelForm):
    class Meta:
        model = DBImport
        fields = ['file']
