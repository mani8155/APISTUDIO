from django import forms


class ApiMetaForm(forms.Form):
    api_name = forms.CharField(label="Api Name")
    uid = forms.CharField(label="Uid", disabled=True)
    api_type = forms.ChoiceField(label="Api Type", choices=[('rest', 'REST')])
    api_method = forms.ChoiceField(label="Api Method", choices=[('get', 'GET'), ('post', 'POST'), ('put', 'PUT'), ('delete', 'DELETE')])
    code_name = forms.FileField(required=True)
    document_url = forms.CharField(label="Url", required=False)

    def __init__(self, *args, **kwargs):
        super(ApiMetaForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['api_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['api_method'].widget.attrs.update({'class': 'form-select'})
        self.fields['code_name'].widget.attrs.update({'accept': '.py'})


class EditApiMetaForm(forms.Form):
    api_name = forms.CharField(label="Api Name", disabled=True)
    uid = forms.CharField(label="Uid", disabled=True)
    api_type = forms.ChoiceField(label="Api Type", choices=[('rest', 'REST')], disabled=True)
    api_method = forms.ChoiceField(label="Api Method", choices=[('get', 'GET'), ('post', 'POST'), ('put', 'PUT'), ('delete', 'DELETE')], disabled=True)
    code_name = forms.FileField(required=True)
    document_url = forms.CharField(label="Url", required=False)

    def __init__(self, *args, **kwargs):
        super(EditApiMetaForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['api_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['api_method'].widget.attrs.update({'class': 'form-select'})
        self.fields['code_name'].widget.attrs.update({'accept': '.py'})


class RevertApiMetaForm(forms.Form):
    mig_id = forms.CharField()
    uid = forms.CharField()


class CopyCustomForm(forms.Form):
    api_name = forms.CharField(label="Api Name")
    uid = forms.CharField(label="Uid", disabled=True)
    api_type = forms.ChoiceField(label="Api Type", choices=[('rest', 'REST')])
    api_method = forms.ChoiceField(label="Api Method", choices=[('get', 'GET'), ('post', 'POST'), ('put', 'PUT'), ('delete', 'DELETE')])
    api_code_name = forms.CharField(label="Python File", disabled=True)
    document_url = forms.CharField(label="Url", required=False)

    def __init__(self, *args, **kwargs):
        super(CopyCustomForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['api_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['api_method'].widget.attrs.update({'class': 'form-select'})
