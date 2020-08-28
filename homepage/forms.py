from django import forms
from homepage.models import Ticket


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)


class AddTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']
    # title = forms.CharField(max_length=50)
    # description = forms.CharField(widget=forms.Textarea)
