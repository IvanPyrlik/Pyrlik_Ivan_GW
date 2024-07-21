from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from users.models import User
from django import forms


class UserForm(UserCreationForm):
    """
    Форма пользователя.
    """
    class Meta:
        model = User
        fields = ['phone', 'password', 'avatar', 'country', 'first_name', 'last_name']

    #def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)
        #self.fields['password'].widget = forms.HiddenInput()
        #for field_name, field in self.fields.items():
            #if field_name not in ['avatar', 'is_active']:
                #field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(UserCreationForm):
    """
    Регистрация пользователя.
    """
    class Meta:
        model = User
        fields = ('phone', 'avatar', 'country', 'first_name', 'last_name')

    def clean_phone(self):
        """
        Проверка номера телефона.
        """
        data = self.data['phone']

        if len(data) != 11:
            raise forms.ValidationError(f'Номер телефона должен состоять из 11 цифр, а не из {len(data)}')
        elif not data.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять только из цифр')
        elif int(data[0]) != 8:
            raise forms.ValidationError('Номер телефона должен начинаться с 8...')

        return data


class GetKeyForm(forms.Form):
    """
    Получение ключа от пользователя.
    """
    phone = forms.CharField(widget=forms.TextInput())
    key = forms.CharField(widget=forms.TextInput())


class RepeatKeyForm(forms.Form):
    """
    Повторная отправка ключа.
    """
    phone = forms.CharField(widget=forms.TextInput())
