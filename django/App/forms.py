from django import forms
from App.models import Clip

class NewClipForm(forms.Form):
    class Meta:
        widgets = {
            'clip_file': forms.TextInput(attrs={'class': 'myfieldclass'}),
        }
    clip_link = forms.CharField(
        label='Clip URL:',
        required=False)
    clip_file = forms.FileField(
        label='Select a file',
        help_text='',
        required=False)
