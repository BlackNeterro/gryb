from django import forms
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.template.loader import render_to_string
from .models import Order


from .models import Cart, Comment, Product, CarouselImage, User

class RegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=50, label='Имя')
    email = forms.EmailField(required=True, label='Емайл')
    phone_number = forms.CharField(max_length=20, label='Ваш номер телефона')
    address = forms.CharField(max_length=255, label='Ваш адрес')

    class Meta:
        model = User
        fields = ('name', 'email', 'phone_number', 'address', 'password1', 'password2')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'address')


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': ''}


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('quantity',)
        labels = {'quantity': 'Количество'}


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'address')

class OrderForm(forms.ModelForm):
    name = forms.CharField(max_length=50, label='Имя')
    postal_code = forms.CharField(max_length=10, label='Почтовый индекс')
    city = forms.CharField(max_length=100, label='Город')
    address = forms.CharField(max_length=255, label='Адрес')
    recipient_name = forms.CharField(max_length=50, label='Имя получателя')
    recipient_phone = forms.CharField(max_length=20, label='Номер телефона получателя')
    recipient_email = forms.EmailField(label='Email получателя')
    
    class Meta:
        model = Order
        fields = ['name', 'postal_code', 'city', 'address', 'recipient_name', 'recipient_phone', 'recipient_email']