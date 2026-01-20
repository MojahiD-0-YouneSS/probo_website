from django import forms
from apps.core.models import (
    MenuItem,
)

class MenuItemForm(forms.ModelForm):
    class Meta:
        model=MenuItem
        fields = ['name','category','description','price', 'is_available', 'is_vegetarian', 'is_spicy',]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' e.g., Truffle Arancini'
            }),

            'category': forms.Select(attrs={
                'class': 'form-select'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the ingredients and taste...'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',  # Allow cents
                'placeholder': '0.00'
            }),

            # Checkboxes need different Bootstrap styling
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input ms-2',
                'role': 'switch'  # Optional: Makes it look like a toggle switch
            }),

            'is_vegetarian': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
            'is_spicy': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
        }


class QuantityForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 80px; display: inline-block;'
        })
    )
    obj_id = forms.IntegerField(widget=forms.HiddenInput())
