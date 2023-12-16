from django import forms
from .models import Shift_post, Shifter

class ShiftPostForm(forms.ModelForm):
    class Meta:
        model = Shift_post
        fields = ['title', 'content']


class ShifterProfileForm(forms.ModelForm):
    class Meta:
        model = Shifter
        fields = ['bio']