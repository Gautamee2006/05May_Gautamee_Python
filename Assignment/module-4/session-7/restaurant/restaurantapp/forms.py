from django import forms
from .models import Restaurant

class RestaurantForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = ['name', 'cuisine', 'rating']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter Restaurant Name'
            }),
            'rating': forms.NumberInput()
            #'rating': forms.NumberInput(attrs={
            #    'min': 1,
            #    'max': 5
            #}),

        }
    def clean_name(self):
        name = self.cleaned_data['name']

        if len(name) < 3:
            raise forms.ValidationError("Restaurant name must be at least 3 characters.")

        return name

    def clean_rating(self):
        rating = self.cleaned_data['rating']

        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")

        return rating    