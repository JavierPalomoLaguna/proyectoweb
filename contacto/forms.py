from django import forms

class FormularioContacto(forms.Form):
    name = forms.CharField(
    label="Nombre",
    required=True,
    max_length=80,
    widget=forms.TextInput(attrs={'class': 'form-control'})
)
    email = forms.EmailField(
    label="Email",
    required=True,
    widget=forms.EmailInput(attrs={'class': 'form-control'})
)
    contenido = forms.CharField(
    label="Contenido",
    required=True,
    max_length=400,
    widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 5,
        'placeholder': 'Escribe tu mensaje aquí...'
    })
)


