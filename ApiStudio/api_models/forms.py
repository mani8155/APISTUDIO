from django import forms
import configparser
import os
import requests as rq
import json


config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

API_URL = config['DEFAULT']['API_URL']

get_api_url = f"{API_URL}getapi/"
post_api_url = f"{API_URL}postapi/"
update_api_url = f"{API_URL}updateapi/"
delete_api_url = f"{API_URL}deleteapi/"


FIELD_DATATYPES = (
    ("string", "String"),
    ("text", "Text"),
    ("integer", "Integer"),
    ("float", "Float"),
    ("boolean", "Boolean"),
    ("email", "Email"),
    ("date", "Date"),
    ("time", "Time"),
    ("password", "Password"),
    ("single_select", "Single Select"),
    ("multi_select", "Multi Select"),
    ("grid", "Grid"),
)

GRID_FIELD_TYPES = (
    ("character", "Character"),
    ("numeric", "Numeric"),
    ("boolean", "Boolean"),
    ("email", "Email"),
    ("date", "Date"),
    ("time", "Time"),
)


class TableForm(forms.Form):
    table_name = forms.CharField(label="Table Name")
    uid = forms.CharField(label="UID", disabled=True)
    table_name_public = forms.CharField(label="Description")
    document_url = forms.CharField(label="Url", required=False)

    def __init__(self, *args, **kwargs):
        super(TableForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class EditTableForm(forms.Form):
    table_name = forms.CharField(label="Table Name", disabled=True)
    uid = forms.CharField(label="UID", disabled=True)
    table_name_public = forms.CharField(label="Description")
    document_url = forms.CharField(label="Url", required=False)

    def __init__(self, *args, **kwargs):
        super(EditTableForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class FieldForm(forms.Form):
    field_name = forms.CharField(label="Field Name")
    field_name_public = forms.CharField(label="Description")
    field_data_type = forms.ChoiceField(label="Field Data Type", choices=FIELD_DATATYPES)
    related_to = forms.HiddenInput()

    def __init__(self, *args, **kwargs):
        super(FieldForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['field_data_type'].widget.attrs.update({'class': 'form-select'})





class EditFieldForm(forms.Form):
    field_name = forms.CharField(label="Field Name", disabled=True)
    field_name_public = forms.CharField(label="Description")
    field_data_type = forms.ChoiceField(label="Field Data Type", choices=FIELD_DATATYPES)
    related_to = forms.HiddenInput()

    def __init__(self, *args, **kwargs):
        super(EditFieldForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['field_data_type'].widget.attrs.update({'class': 'form-select'})


DATE_FORMAT = (
    ("%d-%m-%Y", "DD-MM-YYYY"),
)


class DatePropertyForm(forms.Form):
    date_format = forms.ChoiceField(label="Date Format", choices=DATE_FORMAT)

    def __init__(self, *args, **kwargs):
        super(DatePropertyForm, self).__init__(*args, **kwargs)

        self.fields['date_format'].widget.attrs.update({'class': 'form-select'})


PASSWORD_HASHES = (
    ("md5", "MD5"),
)


class PasswordPropertyForm(forms.Form):
    encryption = forms.ChoiceField(label="Date Format", choices=PASSWORD_HASHES)

    def __init__(self, *args, **kwargs):
        super(PasswordPropertyForm, self).__init__(*args, **kwargs)

        self.fields['encryption'].widget.attrs.update({'class': 'form-select'})


class StringPropertyForm(forms.Form):
    unique = forms.BooleanField(label="Unique", required=False, initial=False)
    nullable = forms.BooleanField(label="Nullable", required=False)

    def __init__(self, *args, **kwargs):
        super(StringPropertyForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-check-input'})


class ApiAllowedMethodsForm(forms.Form):
    get_api = forms.BooleanField(label="Get Api", required=False, help_text=get_api_url)
    post_api = forms.BooleanField(label="Post Api", required=False, help_text=post_api_url)
    update_api = forms.BooleanField(label="Update Api", required=False, help_text=update_api_url)
    delete_api = forms.BooleanField(label="Delete Api", required=False, help_text=delete_api_url)

    def __init__(self, *args, **kwargs):
        super(ApiAllowedMethodsForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-check-input'})


class SelectForm(forms.Form):
    choice = forms.CharField(label="Choice")

    def __init__(self, *args, **kwargs):
        super(SelectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class GridForm(forms.Form):
    column_name = forms.CharField(label="Column Name")
    column_type = forms.ChoiceField(label="Column Type", choices=GRID_FIELD_TYPES)

    def __init__(self, *args, **kwargs):
        super(GridForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['column_type'].widget.attrs.update({'class': 'form-select'})
        
        
class OtherPropertyForm(forms.Form):
    nullable = forms.BooleanField(label="Nullable", required=False)
    
    def __init__(self, *args, **kwargs):
        super(OtherPropertyForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-check-input'})


class ImportForm(forms.Form):
    import_file = forms.FileField(required=True)

    def __init__(self, *args, **kwargs):
        super(ImportForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['import_file'].widget.attrs.update({'accept': '.xlsx'})


class ImportExcelForm(forms.Form):
    api_url = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(ImportExcelForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
