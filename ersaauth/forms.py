from django import forms
from django.conf import settings

from django.core.exceptions import ValidationError

import re

reg_pwd_strength = getattr(settings,
                                      'REG_PWD_STRENGTH',
                                      '^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*[!@#\$%\^&\*]).{8,}')

STRENGTH_VALIDATOR = re.compile(reg_pwd_strength)

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
        'weak_password': "The strength of password is weak.",
    }
    new_password1 = forms.CharField(label="New password",
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="New password confirmation",
                                    widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )

            if not STRENGTH_VALIDATOR.match(password2):
                raise forms.ValidationError(
                    self.error_messages['weak_password'],
                    code='weak_password',
                )
        return password2
