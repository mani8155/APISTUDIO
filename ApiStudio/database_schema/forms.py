from django import forms


class AddSchemaForm(forms.Form):
    schema_name = forms.CharField(label='Schema Name')

    def __init__(self, *args, **kwargs):
        super(AddSchemaForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})



class DBPasswordForm(forms.Form):
    password = forms.CharField(label='DB Password', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(DBPasswordForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})