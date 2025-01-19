from django import forms


class MyForm(forms.Form):
    form_title = forms.CharField().required
    form_description = forms.CharField().required
    question = forms.CharField().required
    reponse = forms.CharField().required


    def clean_reponse(self):
        reponse = self.data.getlist('name[]')
        return reponse

    def clean_question(self):
        question = self.data.getlist('question[]')
        if question is None:
            raise forms.ValidationError("Question is required")
        return question





