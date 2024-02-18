# RIVUE/forms.py
from django import forms
from .models import RIVUE

class RIVUEForm(forms.ModelForm):
    class Meta:
        model = RIVUE
        fields = ['ProModel', 'ProName', 'ProRev', 'ProEmail', 'ProCom', 'ProImage']
