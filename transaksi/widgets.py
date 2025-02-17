from django import forms

class PhoneNumberWidget(forms.TextInput):
    template_name = 'widgets/phone_number.html'

    def __init__(self, attrs=None):
        default_attrs = {'placeholder': 'Nomor HP'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

    def format_value(self, value):
        # Ensure the displayed value includes the prefix, but save only the part entered by the user.
        if value and value.startswith('+62'):
            value = value[3:]  # Remove the '+62' part for display
        return value
