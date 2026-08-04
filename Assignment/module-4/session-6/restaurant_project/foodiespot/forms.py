from django import forms

class AddRestaurantForm(forms.Form):
    restaurant_name = forms.CharField(max_length=100)
    cuisine_type = forms.CharField(max_length=100)
    contact_email = forms.EmailField()

    def clean_restaurant_name(self):
        name = self.cleaned_data['restaurant_name']

        if len(name) < 3:
            raise forms.ValidationError("Restaurant name must be at least 3 characters.")

        return name