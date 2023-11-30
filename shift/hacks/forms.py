from django import forms
from .models import Shift_post

class ShiftPostForm(forms.ModelForm):
    class Meta:
        model = Shift_post
        fields = ['title', 'content']
