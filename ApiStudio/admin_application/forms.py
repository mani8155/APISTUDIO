from django import forms


class ApplicationParentGroupForm(forms.Form):
    name = forms.CharField(label="Name")
    group_id = forms.CharField(label="Group ID")
    child = forms.BooleanField(widget=forms.HiddenInput(), required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(ApplicationParentGroupForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class ApplicationGroupForm(forms.Form):
    name = forms.CharField(label="Name")
    group_id = forms.CharField(label="Group ID")
    child = forms.BooleanField(widget=forms.HiddenInput(), required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super(ApplicationGroupForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class ParentApplicationGroupForm(forms.Form):
    name = forms.CharField(label="Name")
    group_id = forms.CharField(label="Group ID")

    def __init__(self, *args, **kwargs):
        super(ParentApplicationGroupForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


APPLICATION_TYPES = (
    ("custom_api", "Custom Api"),
    ("core_api", "Core Api"),
    ("model", "Model"),
    ("html", "HTML"),
    ("markdown", "Markdown"),
    ("platform", "Platform"),
)


class ApplicationForm(forms.Form):
    name = forms.CharField(label="Name")
    app_id = forms.CharField(label="App ID")
    type = forms.ChoiceField(label='Type', choices=APPLICATION_TYPES)
    used = forms.BooleanField(label="Used", widget=forms.HiddenInput(), required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['type'].widget.attrs.update({'class': 'form-select'})


class EditApplicationForm(forms.Form):
    name = forms.CharField(label="Name")
    app_id = forms.CharField(label="App ID")
    type = forms.ChoiceField(label='Type', choices=APPLICATION_TYPES)

    def __init__(self, *args, **kwargs):
        super(EditApplicationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['type'].widget.attrs.update({'class': 'form-select'})
        self.fields['app_id'].widget.attrs.update({'readonly': True})


class ImportApplicationForm(forms.Form):
    import_url = forms.CharField(label="Import From")
