from django import forms


class UserPrivilegeForm(forms.Form):
    user_privilege_name = forms.CharField(label='User Privilege')
    menu_items = forms.MultipleChoiceField(label="Menu Items")
    menu_privilege = forms.ChoiceField(label='Menu Name')

    def __init__(self, *args, **kwargs):
        super(UserPrivilegeForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class RolesMasterForm(forms.Form):
    user_role = forms.CharField(label="Role Name")
    user_role_privilege = forms.MultipleChoiceField(label="User Privilege", required=True)
    active = forms.BooleanField(label="Active", required=False)

    def __init__(self, *args, **kwargs):
        super(RolesMasterForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['active'].widget.attrs.update({'class': 'form-check-input'})


class UserMasterForm(forms.Form):
    USER_TYPES = [('User', 'User'), ('Admin', 'Admin')]
    username = forms.CharField(label="Username")
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.CharField(label="Email")
    reporting_to = forms.CharField(label="Reporting To")
    user_roles = forms.MultipleChoiceField(label="User Roles")
    user_type = forms.ChoiceField(label="User Type", choices=USER_TYPES)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserMasterForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.CharField(label="Email")
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class PasswordResetForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


# class MenuElementsForm(forms.Form):
#     menu_app_bar = forms.ChoiceField(label="Menu App Bar",
#                                      choices=[('Sidebar Menu', 'Sidebar Menu'), ('Topbar Menu', 'Topbar Menu')])
#     menu_name = forms.CharField(label="Menu Name")
#     menu_type = forms.MultipleChoiceField(label="Menu Type",
#                                           choices=[('Link', 'Link'), ('Dropdown', 'Dropdown')])
#     menu_href = forms.CharField(label="Href")
#     menu_icon = forms.CharField(label="Icon")
#     menu_order = forms.IntegerField(label="Menu Order", initial=0)
#     menu_level = forms.IntegerField(label="Menu Level", initial=0)
#     active = forms.ChoiceField(label="Active", required=False, choices=[('Active', 'Active'), ('In-Active', 'In-Active')])
#     menu_psk_id = forms.IntegerField(label='menu_psk_id')
#     menu_psk_uid = forms.CharField(label='menu_psk_uid')
#     menu_uid = forms.CharField(label='menu_uid')
#
#     def __init__(self, *args, **kwargs):
#         super(MenuElementsForm, self).__init__(*args, **kwargs)
#
#         for name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'form-control'})


class MenuElementsForm(forms.Form):
    menu_name = forms.CharField(label="Menu Name")
    active = forms.ChoiceField(label="Active", required=False,
                               choices=[('Active', 'Active'), ('In-Active', 'In-Active')])
    menu_uid = forms.CharField(label='menu_uid')

    def __init__(self, *args, **kwargs):
        super(MenuElementsForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            self.fields['menu_uid'].widget.attrs['readonly'] = True


class EditMenuElementsForm(forms.Form):
    menu_name = forms.CharField(label="Menu Name")
    active = forms.ChoiceField(label="Active", required=False,
                               choices=[('Active', 'Active'), ('In-Active', 'In-Active')])
    menu_uid = forms.CharField(label='menu_uid')
    menu_order = forms.IntegerField(label="Menu Order")

    def __init__(self, *args, **kwargs):
        super(EditMenuElementsForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            self.fields['menu_uid'].widget.attrs['readonly'] = True
            self.fields['menu_order'].widget.attrs['readonly'] = True


class MenuPrivilegeForm(forms.Form):
    menu_privilege_name = forms.CharField(label="Menu Privilege Name")
    # active = forms.ChoiceField(label="Active", required=False,
    #                            choices=(("Active", "Active"), ("In-Active", "In-Active")))
    menu_privilege_start_date = forms.DateField(label="Menu Privilege Start Date",
                                                widget=forms.DateInput(attrs={'type': 'date'}))
    menu_privilege_end_date = forms.DateField(label="Menu Privilege End Date",
                                              widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(MenuPrivilegeForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class EditMenuPrivilegeForm(forms.Form):
    menu_privilege_name = forms.CharField(label="Menu Privilege Name")
    active = forms.ChoiceField(label="Active", required=False,
                               choices=(("Active", "Active"), ("In-Active", "In-Active")))
    menu_privilege_start_date = forms.DateField(label="Menu Privilege Start Date",
                                                widget=forms.DateInput(attrs={'type': 'date'}))
    menu_privilege_end_date = forms.DateField(label="Menu Privilege End Date",
                                              widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(EditMenuPrivilegeForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
