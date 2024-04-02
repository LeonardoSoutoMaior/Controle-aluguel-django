from django import forms
from .models import Client


## Cadastra Cliente
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
    
    def __init__(self, *args, **kwargs): #adiciona
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            