from django import forms


class ViewsForm(forms.Form):
    uid = forms.CharField(label="Uid")
    api_name = forms.CharField(label="Api Name")
    api_type = forms.ChoiceField(label="Api Type", choices=[('rest', 'REST')])
    api_method = forms.ChoiceField(label="Api Method", choices=[('post', 'POST')])

    def __init__(self, *args, **kwargs):
        super(ViewsForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['api_type'].widget.attrs.update({'readonly': True})
        self.fields['api_method'].widget.attrs.update({'class': 'form-select'})


class EditViewsForm(forms.Form):
    uid = forms.CharField(label="Uid")
    api_name = forms.CharField(label="Api Name")
    api_type = forms.ChoiceField(label="Api Type", choices=[('rest', 'REST')])
    api_method = forms.ChoiceField(label="Api Method", choices=[('post', 'POST')])
    api_trace = forms.ChoiceField(label="Api Trace", choices=[(True, 'Active'), (False, 'In-Active')])

    def __init__(self, *args, **kwargs):
        super(EditViewsForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['uid'].widget.attrs.update({'readonly': True})
        self.fields['api_method'].widget.attrs.update({'readonly': True})
        self.fields['api_type'].widget.attrs.update({'readonly': True})
