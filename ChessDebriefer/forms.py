from django import forms


class UploadPGNForm(forms.Form):
    file = forms.FileField()
