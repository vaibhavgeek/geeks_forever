from django import forms
from app.models import Uploads

class UploadForm(forms.Form):
    file = forms.FileField(
        label='Select your file',
        help_text='max. 42 megabytes'
    )