from django import forms


class CMSForm(forms.Form):
    cms_page_name = forms.CharField(label="Api Name")
    uid = forms.CharField(label="Uid")
    api_type = forms.ChoiceField(label="Api Type", choices=[('rest', 'REST')])
    # api_method = forms.ChoiceField(label="Api Method", choices=[('get', 'GET'), ('post', 'POST'), ('put', 'PUT'), ('delete', 'DELETE')])
    api_method = forms.ChoiceField(label="Api Method", choices=[('get', 'GET')])
    file_type = forms.CharField(label="File Type")
    md_file = forms.FileField(required=True, label="Python Code")

    def __init__(self, *args, **kwargs):
        super(CMSForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['api_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['api_method'].widget.attrs.update({'class': 'form-select'})
        self.fields['md_file'].widget.attrs.update({'accept': '.md, .html'})
        self.fields['uid'].widget.attrs.update({'readonly': True})
        self.fields['file_type'].widget.attrs.update({'readonly': True})


class UpdateCMSForm(forms.Form):
    api_name = forms.CharField(label="Api Name")
    api_type = forms.CharField(label="Api Type", disabled=True)
    uid = forms.CharField(label="Uid", disabled=True)
    api_method = forms.CharField(label="Api Method", disabled=True)
    file_type = forms.CharField(label="File Type")
    md_file = forms.FileField(required=True)

    def __init__(self, *args, **kwargs):
        super(UpdateCMSForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['md_file'].widget.attrs.update({'accept': '.md, .html'})
        self.fields['file_type'].widget.attrs.update({'readonly': True})


class CopyForm(forms.Form):
    api_name = forms.CharField(label="Api Name")
    api_type = forms.CharField(label="Api Type")
    uid = forms.CharField(label="Uid")
    api_method = forms.CharField(label="Api Method")
    file_type = forms.CharField(label="File Type")
    md_file = forms.CharField(label="File")

    def __init__(self, *args, **kwargs):
        super(CopyForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['file_type'].widget.attrs.update({'readonly': True})
        self.fields['api_type'].widget.attrs.update({'readonly': True})
        self.fields['uid'].widget.attrs.update({'readonly': True})
        self.fields['api_method'].widget.attrs.update({'readonly': True})
        self.fields['md_file'].widget.attrs.update({'readonly': True})


class ChangeApiNameForm(forms.Form):
    api_name = forms.CharField(label="Api Name")
    api_type = forms.CharField(label="Api Type")
    uid = forms.CharField(label="Uid")
    api_method = forms.CharField(label="Api Method")
    file_type = forms.CharField(label="File Type")
    api_code_name = forms.CharField(label="File")

    def __init__(self, *args, **kwargs):
        super(ChangeApiNameForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['file_type'].widget.attrs.update({'readonly': True})
        self.fields['api_type'].widget.attrs.update({'readonly': True})
        self.fields['uid'].widget.attrs.update({'readonly': True})
        self.fields['api_method'].widget.attrs.update({'readonly': True})
        self.fields['api_code_name'].widget.attrs.update({'readonly': True})
