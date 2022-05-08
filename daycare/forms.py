from django import forms
from .models import DayCare, Area
from django.db.models import Max, Min
from django.core.validators import validate_email


class DateInput(forms.DateInput):
    input_type = 'date'


class BookForm(forms.Form):
    dog_name = forms.CharField(required=True, label='Dog guest name',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Enter Dog Name', 'col': 80}))
    email = forms.EmailField(required=True, label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
    start_date = forms.DateField(required=True, label='  Check-in date',
                                 widget=forms.widgets.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(required=True, label='  Check-out date',
                               widget=forms.widgets.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    requests = forms.CharField(required=False, label='Special requests', widget=forms.Textarea
    (attrs={'placeholder': 'Please write your requests here. Special requests cannot be guaranteed – '
                           'but the property will do its best to meet your needs', 'rows': 7, 'cols': 80}))
    agree_terms = forms.BooleanField(required=True, label='I agree with the terms', widget=forms.CheckboxInput)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        email = cleaned_data.get("email")

        if start_date and end_date:
            if end_date < start_date:
                self._errors['end_date'] = self.error_class(["End date should be greater!"])

        return cleaned_data


class DayCareSearchForm(forms.Form):
    min_price = DayCare.objects.all().aggregate(Min('price_per_day')).get('price_per_day__min')
    max_price = DayCare.objects.all().aggregate(Max('price_per_day')).get('price_per_day__max')
    start_date = forms.DateField(required=True, label='  Start date',
                                 widget=forms.widgets.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(required=True, label='  End date',
                               widget=forms.widgets.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    area = forms.ChoiceField(required=False, label='Area',
                             choices=(Area.choices + [('', 'All'), ]), initial="")
    city = forms.CharField(required=False, label='City')
    name = forms.CharField(required=False, label='Day care name')
    price_per_day = forms.ChoiceField(required=False, label='Max price',
                                      choices=((str(x), x) for x in range(min_price, max_price + 11, 10)),
                                      initial=str(max_price))

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if end_date < start_date:
                self._errors['end_date'] = self.error_class(["End date should be greater!"])

        return cleaned_data
