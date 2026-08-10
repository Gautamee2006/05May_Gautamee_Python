from django import forms

from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = [
            'name',
            'price',
            'category',
        ]


        widgets = {

            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter product name'
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'placeholder': 'Enter product price',
                    'step': '0.01'
                }
            ),

            'category': forms.TextInput(
                attrs={
                    'placeholder': 'Enter product category'
                }
            ),
        }