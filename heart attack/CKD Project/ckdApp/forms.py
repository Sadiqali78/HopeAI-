from django import forms
from .models import *


class ckdForm(forms.ModelForm):
    class Meta():
        model=ckdModel
        fields=['age', 'cp', 'thalach', 'exang', 'oldpeak', 'ca']
