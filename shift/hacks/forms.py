from django import forms
from .models import Shift_post, Shifter
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class ShifterCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Shifter
        fields = UserCreationForm.Meta.fields + ('email',)

class UsernameAuthenticationForm(AuthenticationForm):
    pass

class EmailAuthenticationForm(AuthenticationForm):
    email = forms.EmailField()

class ShiftPostForm(forms.ModelForm):
    class Meta:
        model = Shift_post
        fields = ['title', 'content']


class ShifterProfileForm(forms.ModelForm):
    class Meta:
        model = Shifter
        fields = ['nickname', 'bio', 'profile_picture']