from django import forms
from businesslunch.models import OptIn

class OptInForm(forms.ModelForm):

    class Meta:
        model = OptIn
        exclude = {'attendee', 'date'}


class DateForm(forms.Form):
    date = forms.DateField(required=False, widget=forms.TextInput(attrs={'class' : 'span3 datepicker'}))







