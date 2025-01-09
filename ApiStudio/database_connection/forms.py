from django import forms


class DBForm(forms.Form):
    db_engine = forms.ChoiceField(label="DB Engine",
                                  choices=[('mysql', 'MySQL'), ('postgresql', 'PostgreSQL'),
                                           ('mssql', 'MS SQL')])
    db_user = forms.CharField(label="DB User")
    # db_password = forms.CharField(label="DB Password")
    db_password = forms.CharField(label="DB Password", widget=forms.PasswordInput())
    db_host = forms.CharField(label="DB Host")
    db_port = forms.CharField(label="DB Port")
    db_name = forms.CharField(label="DB Name")
    db_connection = forms.CharField(label="DB Connection", required=False)

    def __init__(self, *args, **kwargs):
        super(DBForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['db_engine'].widget.attrs.update({'class': 'form-select'})
