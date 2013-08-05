from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class ProfileForm(forms.ModelForm):
    """
    A form that update user's data like username, email, first name, ...
    """
    username = forms.RegexField(
        label=_("Username"),
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("An username may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})

    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not storred, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

