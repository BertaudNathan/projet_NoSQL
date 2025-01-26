from django import forms


class MyForm(forms.Form):
    form_title = forms.CharField().required
    form_description = forms.CharField().required






