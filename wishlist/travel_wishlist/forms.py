from django import forms
from .models import Place


class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')

# This is a custom form field that inherits from forms.DateInput. 
class DateInput(forms.DateInput):
    input_type = 'date'

class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        
        #widgets is a dictionary that allows you to specify custom widgets for form fields.
        #In this case, we are specifying that the date_visited field should use the DateInput widget,
        #which will render as an HTML5 date input in the form.
        widgets = {
            'date_visited': DateInput()
        }