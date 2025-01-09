from django import forms

SOURCE_KEYS = (
    ("app_group", "App Group"),
    ("app_name", "App Name"),
    ("sql_views", "Sql Views"),
)

EXPIRY_PERIODS = (
    ("minutes", "Minutes"),
    ("hours", "Hours"),
    ("days", "Days"),
    ("months", "Months"),
    ("years", "Years"),
    ("never", "Never"),
)


class AuthenticationForm(forms.Form):

    uid = forms.CharField(label='App ID', disabled=True)
    api_source = forms.ChoiceField(label='Api Source', choices=SOURCE_KEYS, disabled=True)
    expiry_duration = forms.IntegerField(label='Expiry Duration')
    expiry_period = forms.ChoiceField(label='Expiry Period', choices=EXPIRY_PERIODS, required=True)

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['api_source'].widget.attrs.update({'class': 'form-select'})
        self.fields['expiry_period'].widget.attrs.update({'class': 'form-select'})
