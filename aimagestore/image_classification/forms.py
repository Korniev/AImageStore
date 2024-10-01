from django import forms
from django.utils.translation import gettext_lazy as _


class ImageUploadForm(forms.Form):
    image = forms.ImageField(label=_("Upload your image"))
