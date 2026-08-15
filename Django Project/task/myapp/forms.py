from django import forms
from .models import *

class userfrom(forms.ModelForm):
    class Meta:
        model=userinfo
        fields='__all__'
