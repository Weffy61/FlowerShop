from django import forms
from phonenumber_field.formfields import PhoneNumberField

from FlowerApp.models import Order


class ConsultationRequestForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'order__form_input',
                                                                         'placeholder': 'Введите Имя'}))

    phone_number = PhoneNumberField(region='RU', widget=forms.TextInput(attrs={'class': 'order__form_input',
                                                                               'placeholder': '+ 7 (999) 000 00 00'}))

    agree_to_privacy_policy = forms.BooleanField()

    def clean_agree_to_privacy_policy(self):
        agree_to_privacy_policy = self.cleaned_data.get('agree_to_privacy_policy')
        if not agree_to_privacy_policy:
            raise forms.ValidationError('Вы должны согласиться с политикой конфиденциальности.')
        return agree_to_privacy_policy


class OrderForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'order__form_input', 'placeholder': 'Введите Имя'})
    )

    phone_number = PhoneNumberField(
        region='RU',
        widget=forms.TextInput(attrs={'class': 'order__form_input', 'placeholder': '+ 7 (999) 000 00 00'})
    )

    address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'order__form_input', 'placeholder': 'Адрес доставки'})
    )

    delivery_time = forms.ChoiceField(
        choices=Order.DELIVERY_TIME_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'order__form_radio'}))

    class Meta:
        model = Order
        fields = ['client_name', 'phone_number', 'delivery_address', 'delivery_time']
