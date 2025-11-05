from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

from . import models

Contact = models.Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            'first_name', 'last_name', 'phone', 'email', 'description', 'category', 'picture',
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Escreva aqui'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'first_name': 'Primeiro nome',
            'last_name': 'Sobrenome',
            'phone': 'Telefone',
            'email': 'E-mail',
            'description': 'Descrição',
            'category': 'Categoria',
            'picture': 'Imagem',
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            self.add_error(
                'last_name',
                ValidationError(
                    'O sobrenome precisa ser diferente do primeiro nome',
                    code='invalid'
                )
            )


        return super().clean()

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if len(first_name) < 3:
            # raise ValidationError(
            #     'O primeiro nome precisa ter mais de 3 caracteres',
            #     code='invalid'
            # )
            self.add_error(
                'first_name',
                ValidationError(
                'O primeiro nome precisa ter mais de 3 caracteres',
                code='invalid'
            )
        )
        return first_name


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email',
                            ValidationError('Este e-mail ja existe', code='invalid')
                        )
        return email

class RegisterUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='A senha deve ter pelo menos 8 caracteres.',
        required=False
    )
    password2 = forms.CharField(
        label='Confirma Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Digite a mesma senha novamente para confirmação.',
        required=False
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': 'Obrigatório. No máximo, 150 caracteres. Letras, números e @/./+/-/_ apenas.',
            'email': 'Informe um e-mail válido.',
        }

    def save(self, commit = True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)

        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', ValidationError("As senhas não coincidem."))

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error('email',
                            ValidationError('Este e-mail ja existe', code='invalid')
                        )
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1, self.instance)
            except ValidationError as errors:
                self.add_error('password1', ValidationError(errors))

        return password1
