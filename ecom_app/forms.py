from django import forms
from .models import LoginModel

class LoginForm(forms.ModelForm):
    class Meta:
        model = LoginModel
        fields = ['mobile_number', 'email', 'password']
        labels = {
            'mobile_number': 'Mobile Number',
            'email': 'Email',
            'password': 'Password',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        # Hide 'mobile_number' field by default
        self.fields['mobile_number'].widget = forms.HiddenInput()

        # Show 'mobile_number' field if 'email' is not provided
        if 'email' not in self.data:
            self.fields['mobile_number'].widget = forms.TextInput()

        # Hide 'email' field by default
        self.fields['email'].widget = forms.HiddenInput()

        # Show 'email' field if 'mobile_number' is not provided
        if 'mobile_number' not in self.data:
            self.fields['email'].widget = forms.EmailInput()