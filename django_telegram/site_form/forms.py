from .models import SiteModel
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea

class SiteForm(ModelForm):
    class Meta:
        model = SiteModel
        fields = ['name', 'surname', 'text', 'date']

        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            "surname": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            "text": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст'
            }),
            "date": DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата'
            })
        }